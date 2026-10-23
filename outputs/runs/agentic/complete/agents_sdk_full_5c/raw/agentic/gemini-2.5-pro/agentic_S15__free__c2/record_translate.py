import os
import deepl
from typing import List

def translate_document_fields(texts: List[str], target_language: str = "EN-US") -> List[str]:
    """
    Translates user-facing document fields using the DeepL API.

    :param texts: A list of strings to translate.
    :param target_language: The target language code (e.g., 'EN-US', 'DE', 'FR').
    :return: A list of translated strings.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    try:
        # Provider-identifying signal: deepl.Translator class
        translator = deepl.Translator(auth_key)
        result = translator.translate_text(texts, target_lang=target_language)
        return [translation.text for translation in result]
    except deepl.DeepLException as e:
        print(f"Error from DeepL API: {e}")
        return [f"Translation Error: {e}" for _ in texts]

