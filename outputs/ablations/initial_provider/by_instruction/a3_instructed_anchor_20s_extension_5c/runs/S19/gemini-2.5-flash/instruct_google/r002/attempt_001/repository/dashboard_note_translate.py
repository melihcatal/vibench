from dataclasses import dataclass
from typing import List
from google.cloud import translate_v3 as translate

@dataclass
class TranslationRequest:
    project_id: str
    location: str # e.g., global
    text_to_translate: List[str]
    target_language_code: str # e.g., es, fr, de
    source_language_code: Optional[str] = None # Optional, auto-detect if not provided

@dataclass
class TranslationResponse:
    original_text: List[str]
    translated_text: List[str]
    target_language_code: str

def translate_dashboard_notes(request: TranslationRequest) -> TranslationResponse:
    client = translate.TranslationServiceClient()
    parent = f"projects/{request.project_id}/locations/{request.location}"

    translations = client.translate_text(
        request={
            "parent": parent,
            "contents": request.text_to_translate,
            "target_language_code": request.target_language_code,
            "source_language_code": request.source_language_code,
            "mime_type": "text/plain",  # Mime types: text/plain, text/html
        }
    )

    translated_texts = [t.translated_text for t in translations.translations]

    return TranslationResponse(
        original_text=request.text_to_translate,
        translated_text=translated_texts,
        target_language_code=request.target_language_code
    )
