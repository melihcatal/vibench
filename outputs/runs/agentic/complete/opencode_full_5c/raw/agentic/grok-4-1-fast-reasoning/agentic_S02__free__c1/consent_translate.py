import deepl
import os

translator = deepl.Translator(auth_key=os.getenv("DEEPL_AUTH_KEY"))


def translate_consent_copy(
    text: str, source_lang: str = "auto", target_lang: str = "EN-US"
) -> str:
    result = translator.translate_text(
        text, source_lang=source_lang, target_lang=target_lang
    )
    return result.text
