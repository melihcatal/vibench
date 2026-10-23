import os
from typing import TypedDict, List

class TranslateRequest(TypedDict):
    """TypedDict representing the request payload for translation."""
    text: str
    source_language_code: str
    target_language_code: str

class TranslateResponse(TypedDict):
    """TypedDict representing the response payload from translation."""
    translated_text: str

class NormalizedResponse(TypedDict):
    """Normalized response used by downstream utilities."""
    source: str
    target: str
    raw_response: Any

def normalize_response(raw: Mapping[str, Any]) -> NormalizedResponse:
    """Convert provider raw response to a standardized shape."""
    return NormalizedResponse(
        source=raw.get("sourceLanguageCode", ""),
        target=raw.get("targetLanguageCode", ""),
        raw_response=raw,
    )

# Example of wrapping a provider-specific client
class TranslationClient:
    """Local wrapper around a concrete translation provider client."""

    SERVICE_NAME = "google-cloud-translate"

    def __init__(self):
        # Provider-specific initialization (e.g., Google client library)
        pass

    def translate(self, text: str, source_lang: str, target_lang: str) -> TranslateResponse:
        # Provider call – here a placeholder returning a dict
        return {
            "translatedText": f"{text} translated",
            "sourceLanguageCode": source_lang,
            "targetLanguageCode": target_lang,
        }
