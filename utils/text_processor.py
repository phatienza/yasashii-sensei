"""
Yasashii Sensei - Japanese Text Processing Utilities
Helper functions for handling Japanese text.
"""

import re
from typing import Optional


def count_characters(text: str) -> int:
    """
    Count Japanese characters in text (excluding spaces and punctuation).
    
    Args:
        text: Input text
        
    Returns:
        Number of Japanese characters
    """
    # Remove spaces and common punctuation
    cleaned = re.sub(r'[\s、。！？「」『』（）\(\)]+', '', text)
    return len(cleaned)


def has_japanese(text: str) -> bool:
    """
    Check if text contains Japanese characters (hiragana, katakana, or kanji).
    
    Args:
        text: Input text
        
    Returns:
        True if text contains Japanese characters, False otherwise
    """
    # Unicode ranges for Japanese characters
    # Hiragana: 3040-309F
    # Katakana: 30A0-30FF
    # Kanji: 4E00-9FFF
    japanese_pattern = re.compile(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]+')
    return bool(japanese_pattern.search(text))


def truncate_text(text: str, max_length: int = 5000) -> str:
    """
    Truncate text to maximum length, preserving sentence boundaries if possible.
    
    Args:
        text: Input text
        max_length: Maximum length in characters
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    # Try to truncate at sentence boundary (。！？)
    truncated = text[:max_length]
    sentence_endings = ['。', '！', '？', '!', '?', '.']
    
    # Find last sentence ending
    last_ending = -1
    for ending in sentence_endings:
        pos = truncated.rfind(ending)
        if pos > last_ending:
            last_ending = pos
    
    # If found a sentence ending in the last 20% of text, use it
    if last_ending > max_length * 0.8:
        return truncated[:last_ending + 1]
    
    # Otherwise, just truncate at max_length
    return truncated + '...'


def extract_sentences(text: str) -> list:
    """
    Split Japanese text into sentences.
    
    Args:
        text: Input text
        
    Returns:
        List of sentences
    """
    # Split on Japanese sentence endings
    sentences = re.split(r'[。！？]+', text)
    
    # Remove empty strings and strip whitespace
    sentences = [s.strip() for s in sentences if s.strip()]
    
    return sentences


def normalize_text(text: str) -> str:
    """
    Normalize Japanese text (remove extra whitespace, normalize line breaks).
    
    Args:
        text: Input text
        
    Returns:
        Normalized text
    """
    # Replace multiple spaces with single space
    text = re.sub(r'\s+', ' ', text)
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    return text


def is_valid_japanese_text(text: str, min_length: int = 1, max_length: int = 5000) -> tuple:
    """
    Validate Japanese text input.
    
    Args:
        text: Input text
        min_length: Minimum required length
        max_length: Maximum allowed length
        
    Returns:
        Tuple of (is_valid: bool, error_message: Optional[str])
    """
    if not text or not text.strip():
        return False, "Text cannot be empty"
    
    text = text.strip()
    
    if len(text) < min_length:
        return False, f"Text must be at least {min_length} characters"
    
    if len(text) > max_length:
        return False, f"Text must not exceed {max_length} characters"
    
    if not has_japanese(text):
        return False, "Text must contain Japanese characters"
    
    return True, None


def get_text_stats(text: str) -> dict:
    """
    Get statistics about Japanese text.
    
    Args:
        text: Input text
        
    Returns:
        Dictionary with text statistics
    """
    return {
        "total_length": len(text),
        "character_count": count_characters(text),
        "sentence_count": len(extract_sentences(text)),
        "has_japanese": has_japanese(text),
        "has_hiragana": bool(re.search(r'[\u3040-\u309F]', text)),
        "has_katakana": bool(re.search(r'[\u30A0-\u30FF]', text)),
        "has_kanji": bool(re.search(r'[\u4E00-\u9FFF]', text))
    }

# Made with Bob
