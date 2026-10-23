from typing import Dict, Any
import os
from deepl import Translator


class RecordTranslator:
    def __init__(self) -> None:
        self.auth_key = os.getenv("DEEPL_AUTH_KEY")
        self.translator = Translator(self.auth_key)

    def translate_record(
        self, document_data: Dict[str, Any], fields: list[str], target_lang: str
    ) -> Dict[str, Any]:
        translated_data = document_data.copy()
        for field in fields:
            if field in document_data:
                result = self.translator.translate_text(
                    str(document_data[field]), target_lang=target_lang
                )
                translated_data[field] = result.text
        return translated_data
