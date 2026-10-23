from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class TranslationRequest:
    text_content: str
    source_language_code: str
    target_language_code: str
    mime_type: str = "text/plain"

@dataclass
class TranslationResponse:
    translated_text: str
    detected_source_language_code: str

@dataclass
class BatchTranslationRequest:
    text_contents: List[str]
    source_language_code: str
    target_language_code: str
    mime_type: str = "text/plain"

@dataclass
class BatchTranslationResponse:
    translations: List[str]
    detected_source_language_codes: List[str]

def normalize_google_translation_response(
    response_translations: Any,
) -> List[TranslationResponse]:
    """Normalizes Google Cloud Translation API response to a list of TranslationResponse."""
    normalized_responses = []
    for translation in response_translations:
        normalized_responses.append(
            TranslationResponse(
                translated_text=translation.translated_text,
                detected_source_language_code=translation.detected_language_code,
            )
        )
    return normalized_responses
