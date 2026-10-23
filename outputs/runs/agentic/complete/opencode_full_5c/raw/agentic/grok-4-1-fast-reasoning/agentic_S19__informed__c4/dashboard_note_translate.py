import os
import deepl


def dashboard_note_translate(
    text: str, source_lang: str = "EN", target_lang: str = "FR"
) -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(
        text, source_lang=source_lang, target_lang=target_lang
    )
    return result.text
