import os
import deepl


def translate_live_caption(text: str, target_language: str = "FR"):
    """
    Translates a live caption text to the target language using DeepL API.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    try:
        translator = deepl.Translator(auth_key)
        result = translator.translate_text(text, target_lang=target_language)
        return result.text
    except deepl.DeepLException as e:
        print(f"DeepL translation error: {e}")
        return None
