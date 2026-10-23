import os
import re
from google.cloud import translate_v2 as translate

TRANSLATE = translate.Client()

def contains_unsafe_content(text: str) -> bool:
    """Simple unsafe content detector for localized copy.
    Flags profanity, personal data, or malicious links.
    Args:
        text: The localized string to check.
    Returns:
        True if unsafe, False otherwise.
    """
    # Basic profanity list (extend as needed)
    profanity = {'fuck', 'shit', 'bitch', 'asshole'}
    words = re.findall(r'\\b\\w+\\b', text.lower())
    if any(w in profanity for w in words):
        return True
    # Email pattern
    if re.search(r'\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}\\b', text):
        return True
    # Phone number pattern
    if re.search(r'\\b\\d{3}[-.]?\\d{3}[-.]?\\d{4}\\b', text):
        return True
    # Malicious link heuristic
    if re.search(r'https?://(\\S+\.)*(malicious|phish|scam)\\.', text):
        return True
    return False

def unsafe_copy_check(translated_texts: list[str]) -> list[bool]:
    """Check each translated string for unsafe content.
    Returns a parallel list of booleans.
    """
    return [contains_unsafe_content(t) for t in translated_texts]