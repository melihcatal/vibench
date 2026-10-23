from typing import Dict
from database_models import Document
from io import StringIO

# Placeholder for a real content safety check.
# Here we simulate a check by scanning for prohibited keywords.

PROHIBITED = {"credit card", "password", "ssn"}

def scan_for_unsafe_content(doc: Document) -> bool:
    """
    Return True if the document appears safe (no unsafe terms in user fields).
    """
    text_fields = {k: v for k, v in doc["data"].items() if isinstance(v, str)}
    for text in text_fields.values():
        lower = text.lower()
        for bad in PROHIBITED:
            if bad in lower:
                print(f"Unsafe content detected: {bad}")
                return False
    return True
