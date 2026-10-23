import os
import deepl

def translate_record_text(text: str, target_language: str = "EN-US"):
    """
    Translates user-facing document fields using the DeepL API.

    :param text: The text to be translated.
    :param target_language: The target language code (e.g., "EN-US", "DE", "FR").
    :return: The translated text as a string.
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
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise
