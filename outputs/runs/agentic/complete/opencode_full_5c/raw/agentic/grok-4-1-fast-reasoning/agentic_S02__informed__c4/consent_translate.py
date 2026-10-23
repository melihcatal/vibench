import deepl
import os


def translate_consent(
    text: str, target_lang: str = "en", source_lang: str | None = None
) -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY not set")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(
        text, target_lang=target_lang, source_lang=source_lang
    )
    return result.text
