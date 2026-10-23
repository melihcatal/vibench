import os
from typing import Dict, Any, Optional
from google.cloud import translate_v3 as translate
from translation_models import TranslationRequest, BatchTranslationRequest

class TranslationClient:
    def __init__(self):
        self.client = translate.TranslationServiceClient()
        self.parent = f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT_ID')}/locations/global"

    def translate_text(self, request: TranslationRequest) -> Dict[str, Any]:
        response = self.client.translate_text(
            parent=self.parent,
            contents=[request.text],
            mime_type="text/plain" if not request.format_ else request.format_,
            source_language_code=request.source_lang,
            target_language_code=request.target_lang,
            model=request.model,
            glossary_config=request.glossary_id,
        )
        return {"translated_text": response.translations[0].translated_text}

    def batch_translate(self, request: BatchTranslationRequest) -> Dict[str, Any]:
        response = self.client.translate_text(
            parent=self.parent,
            contents=request.texts,
            mime_type="text/plain",
            source_language_code=request.source_lang,
            target_language_code=request.target_lang,
            model=request.model,
            glossary_config=request.glossary_id,
        )
        return {"translated_texts": [t.translated_text for t in response.translations]}

def get_translation_client() -> TranslationClient:
    return TranslationClient()