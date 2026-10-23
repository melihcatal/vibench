import os
import deepl


def translate_record_text(text: str, target_language_code: str = "EN-US"):
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    translator = deepl.Translator(auth_key)

    try:
        result = translator.translate_text(text, target_lang=target_language_code)
        return result.text
    except deepl.DeepLException:
        return None
