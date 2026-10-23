import os
from typing import Optional

from deepl import Translator


class TranslationClient:
    """Client for DeepL API for text translation."""

    def __init__(self):
        self.api_key = os.getenv("DEEPL_AUTH_KEY")
        if not self.api_key:
            raise ValueError("DEEPL_AUTH_KEY environment variable not set")
        self.translator = Translator(self.api_key)

    def translate_text(
        self, text: str, target_lang: str, source_lang: Optional[str] = None
    ) -> str:
        """Translate text using DeepL API."""
        result = self.translator.translate_text(
            text, target_lang=target_lang, source_lang=source_lang
        )
        return result.text


def translate_output(
    text: str, target_lang: str, source_lang: Optional[str] = None
) -> str:
    """Translate generated model output using DeepL API."""
    client = TranslationClient()
    return client.translate_text(text, target_lang, source_lang)
