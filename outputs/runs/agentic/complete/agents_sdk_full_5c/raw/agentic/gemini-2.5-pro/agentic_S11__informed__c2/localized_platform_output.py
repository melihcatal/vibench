import os
import deepl

def translate_text_deepl(text: str, target_lang: str) -> str:
    """
    Translates text to another language using the DeepL API.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")
        
    try:
        translator = deepl.Translator(auth_key)
        result = translator.translate_text(text, target_lang=target_lang)
        return result.text
    except deepl.DeepLException as e:
        print(f"Error during DeepL translation: {e}")
        return ""
