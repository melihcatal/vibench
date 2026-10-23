import dataclasses
from typing import List, Dict, Any

@dataclasses.dataclass
class TranslationRequest:
    text: str
    target_language_code: str
    source_language_code: str = "auto"

@dataclasses.dataclass
class TranslationResponse:
    translated_text: str

def normalize_translation_response(api_response: Dict[str, Any]) -> TranslationResponse:
    """
    Normalizes the raw API response from Google Cloud Translation into a TranslationResponse object.
    Assumes the Google Cloud Translation v3 API response format for text translation.
    """
    if "translations" in api_response and api_response["translations"]:
        translated_text = api_response["translations"][0].get("translatedText", "")
        return TranslationResponse(translated_text=translated_text)
    else:
        # Handle cases where the expected structure might be slightly different or empty
        # This could be extended with more robust error handling or logging
        return TranslationResponse(translated_text="")
