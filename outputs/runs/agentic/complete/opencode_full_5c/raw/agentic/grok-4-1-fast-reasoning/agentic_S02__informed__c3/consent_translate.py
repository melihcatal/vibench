import deepl
import os


def translate_consent_copy(
    text: str, target_lang: str = "EN", source_lang: str = "DE"
) -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(
        text, target_lang=target_lang, source_lang=source_lang
    )
    return result.text
