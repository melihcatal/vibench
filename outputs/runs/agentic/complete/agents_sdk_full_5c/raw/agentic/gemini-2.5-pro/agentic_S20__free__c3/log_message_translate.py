import os
import deepl
from typing import Optional

def translate_log_message(text: str, target_lang: str = "JA") -> Optional[str]:
    """
    Translates a log message to a specified language using the DeepL API.

    Args:
        text: The log message to translate.
        target_lang: The target language code (e.g., "JA" for Japanese, "DE" for German).

    Returns:
        The translated text, or None if translation fails.
    """
    auth_key = os.environ.get("DEEPL_API_KEY")
    if not auth_key:
        print("Error: DEEPL_API_KEY environment variable not set.")
        return None

    try:
        translator = deepl.Translator(auth_key)
        result = translator.translate_text(text, target_lang=target_lang)
        if isinstance(result, deepl.TextResult):
             return result.text
        # Handle case where result is a list of TextResult
        elif isinstance(result, list) and result:
             return result[0].text
        return None

    except deepl.DeepLException as e:
        print(f"An error occurred with the DeepL API: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
