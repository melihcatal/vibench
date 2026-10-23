import os
import deepl


def translate_live_caption(text: str, target_language: str = "FR"):
    """
    Translate live captions into another language using DeepL API.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set")

    translator = deepl.Translator(auth_key)
    try:
        result = translator.translate_text(text, target_lang=target_language)
        return result.text
    except deepl.DeepLException as e:
        print(f"Error during translation: {e}")
        return None
