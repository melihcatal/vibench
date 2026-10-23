import os
import deepl

def translate_consent_text(text: str, target_language_code: str) -> str:
    """
    Translates identity provider consent copy using the DeepL API.

    Args:
        text: The source text to translate.
        target_language_code: The ISO 639-1 code for the target language (e.g., "DE", "FR").

    Returns:
        The translated text.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is not set.")

    try:
        translator = deepl.Translator(auth_key)
        result = translator.translate_text(text, target_lang=target_language_code)
        return result.text
    except deepl.DeepLException as e:
        print(f"Error during DeepL translation: {e}")
        raise
