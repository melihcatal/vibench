# Local configuration and client helper utilities for General Text Translation
import os
from typing import Optional
import deepl
from translation_models import normalize_language_code


class TranslationClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("DEEPL_AUTH_KEY")
        if not self.api_key:
            raise ValueError("DEEPL_AUTH_KEY environment variable not set")
        self.client = deepl.Translator(self.api_key)

    def get_usage(self) -> deepl.Usage:
        return self.client.get_usage()

    def close(self):
        self.client.close()

    def normalize_languages(self, source_lang: Optional[str], target_lang: str) -> tuple[Optional[str], str]:
        normalized_source = normalize_language_code(source_lang) if source_lang else None
        normalized_target = normalize_language_code(target_lang)
        return normalized_source, normalized_target