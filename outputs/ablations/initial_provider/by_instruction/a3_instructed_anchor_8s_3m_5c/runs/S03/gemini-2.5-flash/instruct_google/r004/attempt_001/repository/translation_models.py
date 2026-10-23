from typing import List, Optional, Dict, Any
from dataclasses import dataclass

@dataclass
class TranslationRequest:
    text: List[str]
    target_language: str
    source_language: Optional[str] = None
    mime_type: str = "text/plain"

@dataclass
class TranslationResponse:
    translated_text: List[str]
    original_language: Optional[str] = None

def normalize_translation_response(api_response: Any) -> TranslationResponse:
    """Normalizes the Google Cloud Translation API response into a common format.

    Args:
        api_response: The raw response object from the Google Cloud Translation API.

    Returns:
        A TranslationResponse object containing the translated texts.
    """
    translated_texts = []
    if api_response.translations:
        for translation in api_response.translations:
            translated_texts.append(translation.translated_text)
    # The API response for batch translation doesn't directly provide a single original_language_code
    # if multiple source languages are detected or specified for different texts.
    # For simplicity, we'll omit it or set to None if not easily derivable from a batch response.
    return TranslationResponse(translated_text=translated_texts, original_language=None)
