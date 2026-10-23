from dataclasses import dataclass, field
from typing import List, Optional

# This file serves as a placeholder for custom request/response models
# or normalization helpers if the cloud SDK's models are not sufficient.
# For Google Cloud Translation, the SDK's models are quite comprehensive.

@dataclass
class TranslationRequest:
    contents: List[str]
    target_language_code: str
    source_language_code: Optional[str] = None
    mime_type: str = "text/plain"

@dataclass
class TranslationResponseItem:
    translated_text: str
    detected_language_code: Optional[str] = None

@dataclass
class TranslationResponse:
    translations: List[TranslationResponseItem] = field(default_factory=list)

# Example of a normalization function (not strictly needed for basic translation but shows purpose)
def normalize_translation_response(sdk_response) -> TranslationResponse:
    items = []
    for t in sdk_response.translations:
        items.append(TranslationResponseItem(
            translated_text=t.translated_text,
            detected_language_code=t.detected_language_code
        ))
    return TranslationResponse(translations=items)
