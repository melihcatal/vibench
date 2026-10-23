import json
import re
from typing import Any

def is_payload_safe(plaintext: str) -> bool:
    """Check decrypted text for unsafe content.

    Uses Amazon Comprehend (or a compliant substitute) to detect toxic language.
    Returns False if toxicity is detected, otherwise True.
    
    Args:
        plaintext (str): Decrypted text to evaluate.
    
    Returns:
        bool: True if safe, False if unsafe.
    """
    # Placeholder implementation: simple regex check for profanity / hate speech
    # In real usage replace with a call to AWS Comprehend DetectSentiment / Toxicity API.
    bad_words = ['badword1', 'badword2', 'hate', 'racist', 'sexist']
    lowered = plaintext.lower()
    for w in bad_words:
        if w in lowered:
            return False
    # Regex for overly long repeated characters (spam)
    if re.search(r'(.)\1{5,}', lowered):
        return False
    return True

def evaluate_payload(plaintext: str) -> Dict[str, Any]:
    """Return a dictionary describing safety status and optional cleanup hints."""
    safe = is_payload_safe(plaintext)
    return {
        'safe': safe,
        'details': {
            'contains_sensitive_content': not safe,
            'suggested_action': 'review' if not safe else 'clear'
        }
    }
