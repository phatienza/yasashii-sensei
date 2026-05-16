"""
Yasashii Sensei - AI Prompts and Model Configuration
Centralized location for all watsonx.ai prompts and model settings.
"""

# Model Configuration
PRIMARY_MODEL = "meta-llama/llama-4-maverick-17b-128e-instruct-fp8"
FALLBACK_MODEL = "meta-llama/llama-3-3-70b-instruct"
BANNED_MODELS = ["mistral-medium-2505"]  # Never use for this hackathon

# Model Parameters
MODEL_PARAMS = {
    "max_new_tokens": 1500,
    "temperature": 0.1,
    "top_p": 0.9,
    "repetition_penalty": 1.1
}

# System Context
SYSTEM_CONTEXT = """You are Yasashii Sensei (やさしい先生), an AI Japanese language learning assistant.
Your role is to analyze Japanese text and provide comprehensive learning support for students at various JLPT levels.
Always respond in valid JSON format only, with no additional text or explanations outside the JSON structure."""

# Combined Analysis Prompt (Main MVP Prompt)
COMBINED_ANALYSIS_PROMPT = """Analyze the following Japanese text and provide a comprehensive learning analysis.

Japanese Text:
{japanese_text}

Provide your analysis in VALID JSON format ONLY. Do not include any text before or after the JSON.

Required JSON structure:
{{
  "jlpt_level": "N5|N4|N3|N2|N1",
  "vocabulary": [
    {{
      "word": "Japanese word",
      "reading": "hiragana reading",
      "meaning": "English meaning",
      "jlpt_level": "N5|N4|N3|N2|N1",
      "part_of_speech": "noun|verb|adjective|etc"
    }}
  ],
  "grammar_points": [
    {{
      "pattern": "grammar pattern",
      "explanation": "clear explanation in English",
      "example": "example sentence in Japanese",
      "jlpt_level": "N5|N4|N3|N2|N1"
    }}
  ],
  "translation": "Natural English translation of the entire text",
  "cultural_notes": [
    {{
      "topic": "cultural aspect",
      "explanation": "explanation in English"
    }}
  ]
}}

STRICT ACCURACY RULES:
- Extract individual words only, NEVER include particles
  (は、が、を、に、で、の、へ、と、も) as part of the word
  CORRECT: 月 not 月が
  CORRECT: 綺麗 not 綺麗です
- Only include words that ACTUALLY EXIST in the input text
  NEVER invent or hallucinate words
- Always use full compound readings:
  綺麗 → きれい, 天気 → てんき, 東京 → とうきょう
- Always identify ですね as a grammar pattern when present
- Always identify common patterns: です、ます、ている、
  てください、たい、ない、でしょう、ですね、ますね
- For famous or culturally significant phrases,
  always include the cultural context in cultural_notes

CRITICAL: Return ONLY valid JSON. No markdown, no code blocks, no explanations. Just the JSON object."""

# Fallback Simple Analysis Prompt (if combined fails)
SIMPLE_ANALYSIS_PROMPT = """Analyze this Japanese text and return ONLY valid JSON:

Text: {japanese_text}

JSON format:
{{
  "jlpt_level": "N3",
  "vocabulary": [{{"word": "word", "reading": "reading", "meaning": "meaning", "jlpt_level": "N3", "part_of_speech": "noun"}}],
  "grammar_points": [{{"pattern": "pattern", "explanation": "explanation", "example": "example", "jlpt_level": "N3"}}],
  "translation": "English translation",
  "cultural_notes": [{{"topic": "topic", "explanation": "explanation"}}]
}}

Return ONLY the JSON object, nothing else."""

# Made with Bob
