import os
import deepl

def translate_appeal_text(text: str, target_lang: str = "EN-US") -> str:
    """
    Translates text, such as a user's appeal, into a target language using DeepL.

    Args:
        text: The text to translate.
        target_lang: The target language code (e.g., "EN-US", "DE", "FR").

    Returns:
        The translated text, or the original text if an error occurs.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise EnvironmentError("DEEPL_AUTH_KEY environment variable not set.")

    try:
        translator = deepl.Translator(auth_key)
        result = translator.translate_text(text, target_lang=target_lang)
        return result.text
    except deepl.DeepLException as e:
        print(f"Error during translation with DeepL: {e}")
        return text # Fallback to original text on error
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return text
