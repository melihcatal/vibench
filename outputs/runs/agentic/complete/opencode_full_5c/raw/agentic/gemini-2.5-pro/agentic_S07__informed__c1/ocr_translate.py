import os
import deepl
from document_models import TranslatedText


def translate_text(text: str, target_lang: str = "EN-US") -> TranslatedText:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_lang)

    return TranslatedText(
        text=result.text, detected_source_lang=result.detected_source_lang
    )
