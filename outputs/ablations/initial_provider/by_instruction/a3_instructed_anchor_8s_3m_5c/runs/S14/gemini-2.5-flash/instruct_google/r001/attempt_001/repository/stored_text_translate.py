from google.cloud import translate_v3 as translate
from typing import Optional
from dataclasses import dataclass

@dataclass
class StoredTextTranslateRequest:
    text: str
    target_language: str
    project_id: str

@dataclass
class StoredTextTranslateResponse:
    translated_text: str
    detected_language: Optional[str] = None

def translate_stored_text(request: StoredTextTranslateRequest) -> StoredTextTranslateResponse:
    client = translate.TranslationServiceClient()

    parent = f"projects/{request.project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [request.text],
            "target_language_code": request.target_language,
        }
    )

    translated_text = response.translations[0].translated_text
    detected_language = response.translations[0].detected_language_code

    return StoredTextTranslateResponse(
        translated_text=translated_text,
        detected_language=detected_language
    )
