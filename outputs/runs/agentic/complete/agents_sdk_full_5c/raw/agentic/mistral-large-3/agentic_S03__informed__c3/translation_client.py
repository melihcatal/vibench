import os
from typing import Optional
import deepl

class TranslationClient:
    def __init__(self):
        self.auth_key = os.getenv("DEEPL_AUTH_KEY")
        self.client = deepl.Translator(self.auth_key)

    def get_client(self) -> deepl.Translator:
        return self.client

    def validate_languages(self, source_lang: Optional[str], target_lang: str) -> None:
        if source_lang and source_lang.upper() not in deepl.LanguageCode.__members__:
            raise ValueError(f"Unsupported source language: {source_lang}")
        if target_lang.upper() not in deepl.LanguageCode.__members__:
            raise ValueError(f"Unsupported target language: {target_lang}")