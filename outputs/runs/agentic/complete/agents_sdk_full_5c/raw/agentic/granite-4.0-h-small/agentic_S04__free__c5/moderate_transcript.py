import re
from typing import List

def moderate_transcript(text: str) -> str:
    """Remove or replace profanity and other disallowed content before publishing.
    
    Implementation uses a simple regex blacklist; in production replace with a hosted moderation API.
    """
    blacklist = [
        r'\bshit\b',
        r'\bfuck\b',
        r'\bdamn\b',
    ]
    for pattern in blacklist:
        replacement = '***'  # simple replacement
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text
