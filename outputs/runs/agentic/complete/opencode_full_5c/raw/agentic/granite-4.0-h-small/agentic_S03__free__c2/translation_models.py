# translation_models.py
import json
from typing import List, Dict, Any


def normalize_response(response: dict) -> dict:
    """Normalize DeepL response format to a consistent internal schema."""
    # DeepL returns {'text': ..., 'detected_source_language': ...}
    return {
        "translated_text": response.get("text"),
        "source_language": response.get("detected_source_language", "auto"),
    }


def validate_request(text: str, target_lang: str) -> None:
    """Simple validation for request payload."""
    if not text:
        raise ValueError("Empty text provided")
    if target_lang not in ["EN", "FR", "DE", "ES"]:
        raise ValueError("Unsupported target language")


def build_payload(text: str, target_lang: str, is_html: bool = False) -> dict:
    """Construct payload for external translation client."""
    return {
        "auth_key": os.getenv("DEEPL_API_KEY"),
        "text": text,
        "target_lang": target_lang.upper(),
        "html": is_html,
    }


# Example utility to pretty‑print a list of translated items
def pretty_print(translations: List[dict]) -> str:
    return json.dumps(translations, indent=2)
