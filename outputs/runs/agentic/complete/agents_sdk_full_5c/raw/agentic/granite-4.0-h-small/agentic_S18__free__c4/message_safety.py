import re
from typing import List

# Minimal unsafe content check (e.g., profanity, private data patterns)
UNSAFE_PATTERNS = [
    re.compile(r'(?i)fuck|shit|asshole'),  # profanity example
    re.compile(r'\b\d{3}-\d{2}-\d{4}\b'),  # SSN-like US pattern
    re.compile(r'\b\d{4}[ -]?\d{4}[ -]?\d{4}[ -]?\d{4}\b'),  # Credit card pattern
]

def contains_unsafe_text(text: str) -> bool:
    """Return True if any unsafe pattern matches the text."""
    for pat in UNSAFE_PATTERNS:
        if pat.search(text):
            return True
    return False

# Example usage
if __name__ == '__main__':
    samples = [
        'Order shipped successfully.',
        'Your credit card number is 1234 5678 9012 3456.',
        'This is a bad word: fuck!'
    ]
    for s in samples:
        print(s, '-> unsafe?', contains_unsafe_text(s))
