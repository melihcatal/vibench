"""Request, response, and normalization helpers for General Text Translation."""

from typing import Dict, Any

# Provider identifiers (choose one concrete service)
PROVIDER_NAME = "Google Cloud Translation"  # <provider>
PROVIDER_SDK = "google-cloud-translate"

# ---------------------------------------------------------------------------
# payload normalization functions
# ---------------------------------------------------------------------------


def normalize_translate_text_payload(text: str, target_lang: str = "en") -> Dict:
    """Create provider‑specific payload for translating a single string.
    Args:
        text: Source text.
        target_lang: Target language code.
    Returns:
        Dict that can be sent to the provider SDK or REST API.
    """
    return {"q": text, "target": target_lang}


# ---------------------------------------------------------------------------
# response parsing utilities
# ---------------------------------------------------------------------------
def parse_translate_text_response(response: Any) -> str:
    """Extract translated text from provider response.
    Args:
        response: Raw response object (JSON / SDK object).
    Returns:
        The translated text string.
    """
    # Google Cloud Translation returns a dict with 'translatedText'
    return response.get("translatedText", "")
