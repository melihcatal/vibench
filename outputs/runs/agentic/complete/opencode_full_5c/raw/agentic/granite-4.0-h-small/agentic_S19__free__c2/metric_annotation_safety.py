# [LATER-STEP] metric_annotation_safety.py

import re

def contains_unsafe_text(text: str) -> bool:
    \"\"\"Return True if the text contains any of the unsafe patterns.\n    Unsafe patterns are defined for demonstration (e.g., prohibited words, PII, profanity).\n    \"\"\"
    unsafe_patterns = [
        r"\b(expletive|unacceptable|restricted)\b",
        r"\b(social security|ssn|credit card|pi)\b",
    ]
    for pattern in unsafe_patterns:
        if re.search(pattern, text, flags=re.IGNORECASE):
            return True
    return False

def check_annotation_safety(annotation: str) -> tuple[bool, str]:
    \"\"\"Check a free‑text metric annotation for unsafe content.\n    Returns (is_safe, message) tuple.\n    \"\"\"
    if contains_unsafe_text(annotation):
        return (False, "Annotation contains unsafe content: prohibited or PII terms.")
    return (True, "Annotation passed safety check.")
