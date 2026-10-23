from google.cloud import translate_v2 as translate
from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class StoredTextTranslateRequest:
    text_to_translate: str
    target_language: str
    source_language: Optional[str] = None

@dataclass
class StoredTextTranslateResponse:
    translated_text: str
    detected_source_language: Optional[str] = None
    full_response: Optional[Dict[str, Any]] = None

def translate_stored_text(request: StoredTextTranslateRequest) -> StoredTextTranslateResponse:
    client = translate.Client()

    result = client.translate(
        request.text_to_translate,
        target_language=request.target_language,
        source_language=request.source_language
    )

    return StoredTextTranslateResponse(
        translated_text=result['translatedText'],
        detected_source_language=result.get('detectedSourceLanguage'),
        full_response=result
    )
