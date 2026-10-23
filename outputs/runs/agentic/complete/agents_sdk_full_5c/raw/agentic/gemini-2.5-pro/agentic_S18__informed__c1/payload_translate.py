import os
import deepl

def translate_payload_text(text: str, target_language: str = "EN-US") -> str:
    """
    Translates customer-facing message payload text using the DeepL API.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    try:
        translator = deepl.Translator(auth_key)
        result = translator.translate_text(text, target_lang=target_language)
        return result.text
    except deepl.DeepLException as e:
        print(f"Error during translation with DeepL: {e}")
        raise
