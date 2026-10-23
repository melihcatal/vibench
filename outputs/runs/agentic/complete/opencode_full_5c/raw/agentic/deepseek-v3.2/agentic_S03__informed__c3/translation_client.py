import os
import deepl
from typing import Optional, List, Dict, Any


class TranslationClient:
    def __init__(self, auth_key: Optional[str] = None):
        self.auth_key = auth_key or os.getenv("DEEPL_AUTH_KEY")
        if not self.auth_key:
            raise ValueError(
                "DeepL auth key not provided and DEEPL_AUTH_KEY environment variable not set"
            )
        self.client = deepl.Translator(self.auth_key)

    def translate_text(
        self,
        text: str,
        target_lang: str,
        source_lang: Optional[str] = None,
        formality: Optional[str] = None,
        preserve_formatting: bool = False,
    ) -> str:
        result = self.client.translate_text(
            text=text,
            target_lang=target_lang,
            source_lang=source_lang,
            formality=formality,
            preserve_formatting=preserve_formatting,
        )
        return result.text

    def translate_batch(
        self,
        texts: List[str],
        target_lang: str,
        source_lang: Optional[str] = None,
        formality: Optional[str] = None,
        preserve_formatting: bool = False,
    ) -> List[str]:
        results = self.client.translate_text(
            texts,
            target_lang=target_lang,
            source_lang=source_lang,
            formality=formality,
            preserve_formatting=preserve_formatting,
        )
        return [result.text for result in results]

    def get_usage(self) -> Dict[str, Any]:
        usage = self.client.get_usage()
        return {
            "character_count": usage.character.count,
            "character_limit": usage.character.limit,
            "document_count": usage.document.count if hasattr(usage, "document") else 0,
            "document_limit": usage.document.limit if hasattr(usage, "document") else 0,
        }

    def get_supported_languages(self) -> List[Dict[str, str]]:
        languages = self.client.get_target_languages()
        return [{"code": lang.code, "name": lang.name} for lang in languages]


def get_translation_client() -> TranslationClient:
    return TranslationClient()
