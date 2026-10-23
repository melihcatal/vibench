import os
import deepl

def translate_text(text: str, target_language: str = "FR") -> str:
    """
    Translate generated model output using the DeepL API.
    
    Args:
        text: The text to translate.
        target_language: The target language code (e.g., "FR" for French, "DE" for German).

    Returns:
        The translated text, or an error message.
    """
    try:
        auth_key = os.environ["DEEPL_AUTH_KEY"]
    except KeyError:
        return "Error: DEEPL_AUTH_KEY environment variable not set."

    try:
        translator = deepl.Translator(auth_key)
        result = translator.translate_text(text, target_lang=target_language)
        return result.text
    except deepl.DeepLException as e:
        return f"DeepL API error: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"
