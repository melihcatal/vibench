import deepl
import os
from typing import Dict, Any


class DeepLTranslator:
    """
    Translates customer-facing message payload text using DeepL API.
    """

    def __init__(self):
        self.auth_key = os.getenv("DEEPL_AUTH_KEY")
        self.translator = deepl.Translator(self.auth_key)

    def translate(self, text: str, target_lang: str = "EN-US") -> str:
        """
        Translates the provided text to the target language.

        Args:
            text: The text to translate.
            target_lang: The target language code (e.g., "EN-US", "DE", "FR").

        Returns:
            The translated text.
        """
        result = self.translator.translate_text(text, target_lang=target_lang)
        return result.text


def translate_message(text: str, target_lang: str = "EN-US") -> str:
    """
    Translates a message payload using DeepL API.

    Args:
        text: The text to translate.
        target_lang: The target language code (e.g., "EN-US", "DE", "FR").

    Returns:
        The translated text.
    """
    translator = DeepLTranslator()
    return translator.translate(text, target_lang)
