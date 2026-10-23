# [LATER-STEP] unsafe_copy_check.py
import re

def contains_unsafe_content(text: str) -> bool:
    """Very naive check for unsafe material (e.g., profanity or hate speech)."""
    # Simple regex patterns for demonstration; replace with real moderation model or service.
    profanity_pattern = re.compile(r'\b(badword1|badword2)\b', re.IGNORECASE)
    return bool(profanity_pattern.search(text))


def unsafe_copy_report(localized_texts: List[str]) -> List[str]:
    """Return list of localized copies flagged as unsafe."""
    unsafe_items = []
    for i, txt in enumerate(localized_texts):
        if contains_unsafe_content(txt):
            unsafe_items.append(f'Entry {i} contains unsafe content.')
    return unsafe_items
