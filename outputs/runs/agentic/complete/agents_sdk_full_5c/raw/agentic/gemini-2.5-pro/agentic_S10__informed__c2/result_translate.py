import os
import deepl

def translate_text(text: str, target_language: str = "DE") -> str:
    """
    Translates text to the target language using the DeepL API.

    Requires the DEEPL_AUTH_KEY environment variable.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    try:
        translator = deepl.Translator(auth_key)
        result = translator.translate_text(text, target_lang=target_language)
        return result.text
    except deepl.DeepLException as e:
        print(f"An error occurred during translation with DeepL: {e}")
        return f"Error: {e}"
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return "An unexpected error occurred during translation."
