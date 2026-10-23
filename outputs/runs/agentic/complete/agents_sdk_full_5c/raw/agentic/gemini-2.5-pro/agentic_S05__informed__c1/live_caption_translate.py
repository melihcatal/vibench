import os
import deepl

def translate_caption(text: str, target_language: str = "FR") -> str:
    """
    Translates a live caption text chunk into another language using DeepL.

    Args:
        text: The text to translate.
        target_language: The target language code (e.g., "FR" for French).

    Returns:
        The translated text, or an error message.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is not set.")

    try:
        translator = deepl.Translator(auth_key)
        result = translator.translate_text(text, target_lang=target_language)
        return result.text
    except deepl.DeepLException as e:
        return f"DeepL translation error: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"
