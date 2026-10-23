import os
import deepl

def translate_with_deepl(text: str, target_lang: str = "fr", source_lang: str = None):
    """
    Translates text using the DeepL API.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable must be set.")

    translator = deepl.Translator(auth_key)

    try:
        if source_lang:
            result = translator.translate_text(text, target_lang=target_lang, source_lang=source_lang)
        else:
            result = translator.translate_text(text, target_lang=target_lang)
        return result.text
    except deepl.exceptions.DeepLException as e:
        print(f"Error translating with DeepL: {e}")
        return None
