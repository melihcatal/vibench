import os
import deepl

DEEPL_AUTH_KEY = os.environ.get("DEEPL_AUTH_KEY", "")


def translate_result(
    text: str, target_lang: str = "ES", source_lang: str = "EN"
) -> str:
    if not DEEPL_AUTH_KEY:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")

    translator = deepl.Translator(DEEPL_AUTH_KEY)
    result = translator.translate_text(
        text,
        source_lang=source_lang,
        target_lang=target_lang,
    )
    return result.text
