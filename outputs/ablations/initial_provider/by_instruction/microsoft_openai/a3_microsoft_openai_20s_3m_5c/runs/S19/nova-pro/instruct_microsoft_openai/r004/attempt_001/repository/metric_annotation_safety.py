import re

def is_safe_text(text: str) -> bool:
    unsafe_patterns = [
        r'\b(hate|violence|discrimination)\b',
        r'\b(kill|murder|assault)\b',
        r'\b(pornography|nudity)\b',
        r'\b(suicide|self-harm)\b',
        r'\b(terrorism|extremism)\b'
    ]
    for pattern in unsafe_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return False
    return True

def metric_annotation_safety(annotation: str) -> bool:
    return is_safe_text(annotation)