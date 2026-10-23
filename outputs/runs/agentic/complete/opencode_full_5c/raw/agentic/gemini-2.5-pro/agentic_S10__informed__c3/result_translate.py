import os
import deepl
from model_models import TranslationResponse


def translate_text(text: str, target_lang: str) -> TranslationResponse:
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    translator = deepl.Translator(auth_key)

    result = translator.translate_text(text, target_lang=target_lang)

    return TranslationResponse(
        detected_source_language=result.detected_source_lang, text=result.text
    )
