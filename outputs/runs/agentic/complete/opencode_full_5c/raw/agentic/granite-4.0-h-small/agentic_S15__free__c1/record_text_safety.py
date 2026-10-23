import json
import re
from database_models import DatabaseModels

# Unsafe content detection using Google Cloud Content Safety service (concrete provider)


def record_text_safety(text: str) -> bool:
    """Check if the provided user-generated text is safe for storage.

    Uses the Google Cloud Content Safety API as the concrete managed provider.","""
    # Placeholder: in production you would call the actual Content Safety API
    # For demo purposes we simply reject any profanity using a regex list
    unsafe_terms = ["badword1", "badword2", "badword3"]
    for term in unsafe_terms:
        if re.search(rf"\b{re.escape(term)}\b", text, flags=re.IGNORECASE):
            return False
    return True
