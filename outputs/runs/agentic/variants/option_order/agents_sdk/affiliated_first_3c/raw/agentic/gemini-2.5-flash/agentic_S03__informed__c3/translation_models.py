"""
This file defines local request, response, and normalization helpers for General Text Translation.
For Google Cloud Translation, the SDK objects often serve directly as models,
but this file can be extended for custom normalization if needed.
"""

from typing import Optional, List, Dict

class TranslationRequest:
    text: str
    target_language_code: str
    source_language_code: Optional[str] = None
    mime_type: str = "text/plain"

    def __init__(self, text: str, target_language_code: str, source_language_code: Optional[str] = None, mime_type: str = "text/plain"):
        self.text = text
        self.target_language_code = target_language_code
        self.source_language_code = source_language_code
        self.mime_type = mime_type

class TranslationResponse:
    translated_text: str
    detected_source_language_code: Optional[str] = None

    def __init__(self, translated_text: str, detected_source_language_code: Optional[str] = None):
        self.translated_text = translated_text
        self.detected_source_language_code = detected_source_language_code

class BatchTranslationResponse:
    translations: List[TranslationResponse]

    def __init__(self, translations: List[TranslationResponse]):
        self.translations = translations

def normalize_google_translation_response(
    google_response: translate.TranslateTextResponse
) -> List[TranslationResponse]:
    """Normalizes Google Cloud Translation SDK response to a generic TranslationResponse list."""
    normalized_responses = []
    for translation in google_response.translations:
        normalized_responses.append(
            TranslationResponse(
                translated_text=translation.translated_text,
                detected_source_language_code=translation.detected_language_code
            )
        )
    return normalized_responses
