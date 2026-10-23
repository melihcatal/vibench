import re
from typing import Dict

def is_unsafe(message: Dict[str, any]) -> bool:
    """Check message payload text for unsafe content (e.g., profanity, hate speech).
    For demonstration, uses a simple regex blacklist.
    """
    blacklist = [
        re.compile(r'\b(profanity|obscene)\b', re.IGNORECASE),
        re.compile(r'\b(hate|kill|bomb)\b', re.IGNORECASE),
    ]
    payload = message.get('payload', '')
    if isinstance(payload, str):
        for pat in blacklist:
            if pat.search(payload):
                return True
    return False
