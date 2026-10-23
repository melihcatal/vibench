import os
import deepl

# The DeepL Python library uses the DEEPL_AUTH_KEY environment variable.
auth_key = os.environ.get("DEEPL_AUTH_KEY")
if not auth_key:
    raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

translator = deepl.Translator(auth_key)

def translate_record_text(text: str, target_lang: str = "EN-US") -> str:
    """
    Translates user-facing document fields using the DeepL API.

    Args:
        text: The text to be translated.
        target_lang: The target language code (e.g., "EN-US", "DE", "FR").
                     Defaults to "EN-US".

    Returns:
        The translated text as a string.
    """
    if not text:
        return ""

    try:
        result = translator.translate_text(text, target_lang=target_lang)
        return result.text
    except deepl.DeepLException as e:
        print(f"An error occurred during translation with DeepL: {e}")
        return f"Error: Translation failed. {e}"
