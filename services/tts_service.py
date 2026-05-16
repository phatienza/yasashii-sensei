"""
Yasashii Sensei - Text-to-Speech Service
IBM Watson Text-to-Speech integration for Japanese audio synthesis.
"""

import os
import requests
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Simple in-memory cache for TTS audio
_tts_cache = {}


def synthesize_japanese(text: str) -> Optional[bytes]:
    """
    Synthesize Japanese text to speech using IBM Watson TTS.
    
    Args:
        text: Japanese text to synthesize
    
    Returns:
        Audio bytes (MP3 format) or None on error
    """
    if not text or not text.strip():
        return None
    
    # Check cache first
    cache_key = text.strip()
    if cache_key in _tts_cache:
        print(f"TTS cache hit for text: {cache_key[:50]}...")
        return _tts_cache[cache_key]
    
    # Get credentials from environment
    api_key = os.getenv('IBM_TTS_API_KEY')
    tts_url = os.getenv('IBM_TTS_URL')
    voice = os.getenv('IBM_TTS_VOICE', 'ja-JP_EmiV3Voice')
    
    if not api_key or not tts_url:
        print("TTS Error: Missing IBM_TTS_API_KEY or IBM_TTS_URL")
        return None
    
    try:
        # Construct API endpoint
        endpoint = f"{tts_url}/v1/synthesize?voice={voice}"
        
        # Make API request
        response = requests.post(
            endpoint,
            auth=('apikey', api_key),
            headers={
                'Accept': 'audio/mp3',
                'Content-Type': 'application/json'
            },
            json={'text': text},
            timeout=30
        )
        
        # Check response
        if response.status_code == 200:
            audio_bytes = response.content
            # Cache the result
            _tts_cache[cache_key] = audio_bytes
            print(f"TTS synthesis successful: {len(audio_bytes)} bytes")
            return audio_bytes
        else:
            print(f"TTS Error: HTTP {response.status_code} - {response.text}")
            return None
    
    except requests.exceptions.Timeout:
        print("TTS Error: Request timeout")
        return None
    except requests.exceptions.RequestException as e:
        print(f"TTS Error: Request failed - {str(e)}")
        return None
    except Exception as e:
        print(f"TTS Error: Unexpected error - {str(e)}")
        return None


def clear_cache():
    """Clear the TTS cache."""
    global _tts_cache
    _tts_cache.clear()
    print("TTS cache cleared")


# Made with Bob