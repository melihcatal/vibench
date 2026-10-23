import os
import deepl

def runbook_translate(text: str, target_lang: str = "FR") -> str:
    """
    Translates secret rotation runbook notes into another language using DeepL.

    Args:
        text: The text to translate.
        target_lang: The target language code (e.g., "FR" for French, "DE" for German).

    Returns:
        The translated text.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is not set.")

    try:
        translator = deepl.Translator(auth_key)
        result = translator.translate_text(text, target_lang=target_lang)
        return result.text
    except deepl.DeepLException as e:
        print(f"An error occurred with the DeepL API: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise

