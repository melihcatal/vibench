# corpus_safety.py
import re

def is_safe(text: str) -> bool:
    """Simple heuristic to reject unsafe corpus content before embedding.",
    # Reject very long strings, control characters, or obvious HTML/JS snippets
    if len(text) > 5000:
        return False
    if re.search(r'[\\x00-\\x1F\\x7F]', text):
        return False
    # Basic script tag guard
    if re.search(r'<script', text, re.I):
        return False
    return True