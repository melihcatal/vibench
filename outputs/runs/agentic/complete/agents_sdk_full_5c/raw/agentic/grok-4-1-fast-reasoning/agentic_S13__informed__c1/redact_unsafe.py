from safety_client import get_content_safety_client
from safety_models import get_text_moderation_options

def redact_unsafe(text: str, break_mode: str = "word") -> dict:
    client = get_content_safety_client()
    options = get_text_moderation_options()
    response = client.redact_text(options, text=text, break_mode=break_mode)
    return {
        "redacted_text": response.redacted_text,
        "location_hints": [hint._to_dict() for hint in response.location_hints] if hasattr(response, 'location_hints') else []
    }
