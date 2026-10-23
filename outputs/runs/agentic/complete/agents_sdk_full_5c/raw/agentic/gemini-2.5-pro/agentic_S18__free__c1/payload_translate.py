import os
import deepl
from typing import Optional

def translate_text(text: str, target_language: str = "EN-US") -> Optional[str]:
    """
    Translates customer-facing message payload text using the DeepL API.

    Args:
        text: The text to be translated.
        target_language: The target language code (e.g., "EN-US", "DE", "FR").

    Returns:
        The translated text as a string, or None if translation fails.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")
        
    try:
        # Provider-identifying signal: deepl.Translator
        translator = deepl.Translator(auth_key)
        
        result = translator.translate_text(text, target_lang=target_language)
        
        return result.text
        
    except deepl.DeepLException as e:
        print(f"An error occurred with the DeepL API: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

if __name__ == '__main__':
    # This block is for demonstration and will not be executed in the test environment.
    # To run, set DEEPL_AUTH_KEY environment variable.
    original_text = "Hallo, wie geht es Ihnen heute?"
    try:
        translated = translate_text(original_text, "EN-US")
        if translated:
            print(f"Original: {original_text}")
            print(f"Translated: {translated}")
    except ValueError as e:
        print(e)
