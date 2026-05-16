"""
Yasashii Sensei - watsonx.ai Integration Service
Handles all interactions with IBM watsonx.ai REST API using requests library.
"""
import os
import json
import re
import time
from typing import Optional, Dict, Any
import requests

from config.prompts import (
    PRIMARY_MODEL,
    FALLBACK_MODEL,
    BANNED_MODELS,
    MODEL_PARAMS,
    SYSTEM_CONTEXT,
    COMBINED_ANALYSIS_PROMPT
)


class WatsonxService:
    """Service for analyzing Japanese text using watsonx.ai REST API."""
    
    # IAM token endpoint
    IAM_TOKEN_URL = "https://iam.cloud.ibm.com/identity/token"
    
    # watsonx.ai text generation endpoint
    GENERATION_ENDPOINT = "/ml/v1/text/generation?version=2024-05-31"
    
    def __init__(self, api_key = None, project_id = None, url = None):
        """
        Initialize watsonx.ai service.
        
        Args:
            api_key: IBM Cloud API key
            project_id: watsonx.ai project ID
            url: watsonx.ai endpoint URL
        """
        from dotenv import load_dotenv
        load_dotenv()

        self.api_key = api_key or os.getenv('WATSONX_API_KEY')
        self.project_id = project_id or os.getenv('WATSONX_PROJECT_ID')
        self.url = (url or os.getenv('WATSONX_URL', 'https://us-south.ml.cloud.ibm.com')).rstrip('/')
        self.current_model = PRIMARY_MODEL
        self.using_fallback = False
        
        # IAM token cache
        self._iam_token = None
        self._token_expiry = 0
        
        # Validate model configuration
        if self.current_model in BANNED_MODELS:
            raise ValueError(f"Model {self.current_model} is banned for this hackathon")
    
    def get_iam_token(self) -> str:
        """
        Get IAM bearer token for authentication.
        Caches token and refreshes when expired.
        
        Returns:
            IAM bearer token
            
        Raises:
            Exception: If token retrieval fails
        """
        # Check if cached token is still valid (with 60 second buffer)
        if self._iam_token and time.time() < (self._token_expiry - 60):
            return self._iam_token
        
        # Request new token
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        data = {
            "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
            "apikey": self.api_key
        }
        
        try:
            response = requests.post(
                self.IAM_TOKEN_URL,
                headers=headers,
                data=data,
                timeout=30
            )
            response.raise_for_status()
            
            token_data = response.json()
            self._iam_token = token_data["access_token"]
            
            # Token expires in 3600 seconds (1 hour)
            expires_in = token_data.get("expires_in", 3600)
            self._token_expiry = time.time() + expires_in
            
            return self._iam_token
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to get IAM token: {str(e)}")
        except (KeyError, json.JSONDecodeError) as e:
            raise Exception(f"Invalid IAM token response: {str(e)}")
    
    def _switch_to_fallback(self):
        """Switch to fallback model if primary fails."""
        if self.using_fallback:
            raise Exception("Already using fallback model, cannot switch further")
        
        if FALLBACK_MODEL in BANNED_MODELS:
            raise ValueError(f"Fallback model {FALLBACK_MODEL} is banned")
        
        print(f"Switching from {self.current_model} to fallback model {FALLBACK_MODEL}")
        self.current_model = FALLBACK_MODEL
        self.using_fallback = True
    
    def _extract_json(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Extract JSON from model response, handling various formats.
        
        Args:
            text: Raw response text
            
        Returns:
            Parsed JSON dict or None if parsing fails
        """
        # Try direct JSON parse first
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass
        
        # Try to find JSON in markdown code blocks
        json_pattern = r'```(?:json)?\s*(\{.*?\})\s*```'
        matches = re.findall(json_pattern, text, re.DOTALL)
        if matches:
            try:
                return json.loads(matches[0])
            except json.JSONDecodeError:
                pass
        
        # Try to find JSON object in text
        json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
        matches = re.findall(json_pattern, text, re.DOTALL)
        for match in matches:
            try:
                return json.loads(match)
            except json.JSONDecodeError:
                continue
        
        return None
    
    def _clean_analysis(self, result: Dict[str, Any], original_text: str) -> Dict[str, Any]:
        """
        Clean and validate analysis results.
        
        Args:
            result: Raw analysis result from AI
            original_text: Original Japanese text
            
        Returns:
            Cleaned analysis result
        """
        # Japanese particles to strip from word endings
        particles = ['が', 'は', 'を', 'に', 'で', 'の', 'へ', 'と', 'も', 'ね']
        
        # Clean vocabulary
        if 'vocabulary' in result and isinstance(result['vocabulary'], list):
            cleaned_vocab = []
            seen_words = set()
            
            for item in result['vocabulary']:
                if not isinstance(item, dict):
                    continue
                
                word = item.get('word', '')
                
                # Strip particles from word endings
                for particle in particles:
                    if word.endswith(particle):
                        word = word[:-len(particle)]
                        item['word'] = word
                
                # Fix 月 reading when it appears alone
                if word == '月' and item.get('reading') != 'つき':
                    item['reading'] = 'つき'
                
                # Only include words that exist in original text
                if word and word in original_text:
                    # Remove duplicates
                    if word not in seen_words:
                        seen_words.add(word)
                        cleaned_vocab.append(item)
            
            result['vocabulary'] = cleaned_vocab
        
        # Remove duplicate grammar patterns
        if 'grammar_points' in result and isinstance(result['grammar_points'], list):
            seen_patterns = set()
            cleaned_grammar = []
            
            for pattern in result['grammar_points']:
                if not isinstance(pattern, dict):
                    continue
                
                pattern_key = pattern.get('pattern', '')
                if pattern_key and pattern_key not in seen_patterns:
                    seen_patterns.add(pattern_key)
                    cleaned_grammar.append(pattern)
            
            result['grammar_points'] = cleaned_grammar
        
        return result
    
    def _call_generation_api(self, prompt: str) -> str:
        """
        Call watsonx.ai text generation REST API.
        
        Args:
            prompt: Full prompt to send to model
            
        Returns:
            Generated text response
            
        Raises:
            Exception: If API call fails
        """
        # Get IAM token
        token = self.get_iam_token()
        
        # Prepare request
        url = f"{self.url}{self.GENERATION_ENDPOINT}"
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        payload = {
            "model_id": self.current_model,
            "input": prompt,
            "parameters": {
                "max_new_tokens": MODEL_PARAMS["max_new_tokens"],
                "temperature": MODEL_PARAMS["temperature"],
                "top_p": MODEL_PARAMS["top_p"],
                "repetition_penalty": MODEL_PARAMS.get("repetition_penalty", 1.0)
            },
            "project_id": self.project_id
        }
        
        try:
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            
            result = response.json()
            
            # Extract generated text from response
            if "results" in result and len(result["results"]) > 0:
                generated_text = result["results"][0].get("generated_text", "")
                return generated_text
            else:
                raise ValueError("No generated text in API response")
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")
        except (KeyError, json.JSONDecodeError, ValueError) as e:
            raise Exception(f"Invalid API response: {str(e)}")
    
    def analyze_text(self, japanese_text: str, retry_with_fallback: bool = True) -> Dict[str, Any]:
        """
        Analyze Japanese text using watsonx.ai.
        
        Args:
            japanese_text: Japanese text to analyze
            retry_with_fallback: Whether to retry with fallback model on failure
            
        Returns:
            Analysis results as dictionary
            
        Raises:
            Exception: If analysis fails
        """
        # Prepare prompt
        prompt = COMBINED_ANALYSIS_PROMPT.format(japanese_text=japanese_text)
        full_prompt = f"{SYSTEM_CONTEXT}\n\n{prompt}"
        
        try:
            # Call generation API
            response_text = self._call_generation_api(full_prompt)
            
            # Extract JSON from response
            result = self._extract_json(response_text)
            
            if result is None:
                raise ValueError("Failed to extract valid JSON from model response")
            
            # Validate required fields
            required_fields = ["jlpt_level", "vocabulary", "grammar_points", "translation"]
            missing_fields = [field for field in required_fields if field not in result]
            
            if missing_fields:
                raise ValueError(f"Missing required fields in response: {missing_fields}")
            
            # Clean and validate the analysis
            result = self._clean_analysis(result, japanese_text)
            
            # Add metadata
            result["_metadata"] = {
                "model_used": self.current_model,
                "using_fallback": self.using_fallback
            }
            
            return result
            
        except Exception as e:
            # Try fallback model if enabled and not already using it
            if retry_with_fallback and not self.using_fallback:
                print(f"Primary model failed: {str(e)}. Trying fallback model...")
                try:
                    self._switch_to_fallback()
                    return self.analyze_text(japanese_text, retry_with_fallback=False)
                except Exception as fallback_error:
                    raise Exception(f"Both models failed. Primary: {str(e)}, Fallback: {str(fallback_error)}")
            
            raise Exception(f"Text analysis failed: {str(e)}")
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about current model configuration.
        
        Returns:
            Dictionary with model information
        """
        return {
            "current_model": self.current_model,
            "primary_model": PRIMARY_MODEL,
            "fallback_model": FALLBACK_MODEL,
            "using_fallback": self.using_fallback,
            "banned_models": BANNED_MODELS,
            "model_params": MODEL_PARAMS,
            "token_cached": self._iam_token is not None,
            "token_expires_in": max(0, int(self._token_expiry - time.time())) if self._iam_token else 0
        }

# Made with Bob
