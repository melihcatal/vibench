from typing import Dict
import os
from deepl import Translator
from deepl.exceptions import DeepLException


class ScriptTranslator:
    """Translates narration scripts using DeepL API."""

    def __init__(self):
        self.translator = Translator(os.getenv("DEEPL_AUTH_KEY"))

    def translate_script(
        self, text: str, target_lang: str = "EN-US", source_lang: str = None
    ) -> str:
        """
        Translates a narration script to the target language.

        Args:
            text: The text to translate.
            target_lang: The target language code (e.g., "EN-US").
            source_lang: The source language code (e.g., "DE").

        Returns:
            str: The translated text.

        Raises:
            DeepLException: If the translation fails.
        """
        result = self.translator.translate_text(
            text, target_lang=target_lang, source_lang=source_lang
        )
        return result.text
