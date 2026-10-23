from google.cloud import translate_v2 as translate
import os
from typing import Dict, Any


class RecordTranslator:
    def __init__(self):
        self.client = translate.Client()

    def translate_text(self, text: str, target_language: str) -> str:
        result = self.client.translate(text, target_language=target_language)
        return result["translatedText"]

    def translate_document_fields(
        self, document: Dict[str, Any], fields: List[str], target_language: str
    ) -> Dict[str, Any]:
        translated_doc = document.copy()
        for field in fields:
            if field in document:
                translated_doc[field] = self.translate_text(
                    str(document[field]), target_language
                )
        return translated_doc
