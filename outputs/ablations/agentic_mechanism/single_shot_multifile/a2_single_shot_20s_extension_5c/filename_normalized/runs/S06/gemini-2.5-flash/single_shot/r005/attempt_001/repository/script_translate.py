import os
import deepl

def translate_script(text: str, target_lang: str = "en", source_lang: str = None) -> str:
    deepl_auth_key = os.environ.get("DEEPL_AUTH_KEY")

    if not deepl_auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    translator = deepl.Translator(deepl_auth_key)

    result = translator.translate_text(
        text,
        target_lang=target_lang,
        source_lang=source_lang
    )

    return result.text
