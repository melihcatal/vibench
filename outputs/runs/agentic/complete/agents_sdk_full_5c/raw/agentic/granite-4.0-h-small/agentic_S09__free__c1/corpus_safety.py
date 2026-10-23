# Pre-check corpus texts before embedding to avoid unsafe content
import re

SAFE_PATTERNS = [
    re.compile(r'(?:\b|_)(?:hate|kill|weapon|terrorism|porn|drugs|suicide)\b', re.IGNORECASE)
]

def is_corpus_safe(text: str) -> bool:
    """Return True if the text does not contain disallowed terms."""
    lowered = text.lower()
    for pattern in SAFE_PATTERNS:
        if pattern.search(lowered):
            return False
    return True

# Example usage:
# if not is_corpus_safe(user_provided_text): raise ValueError('Unsafe content')
