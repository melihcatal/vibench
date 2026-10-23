import os
import deepl
from typing import Optional

def translate_consent_text(text: str, target_language: str) -> Optional[str]:
    """
    Translates consent screen text using the DeepL API.

    Args:
        text: The source text to translate.
        target_language: The target language code (e.g., "DE", "FR", "ES").
                         Use "EN-US" or "EN-GB" for English variants.

    Returns:
        The translated text, or None if an error occurs.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    try:
        translator = deepl.Translator(auth_key)
        
        # Ensure target language is supported
        supported_languages = [lang.code for lang in translator.get_target_languages()]
        if target_language.upper() not in supported_languages:
            # Fallback or specific handling for unsupported languages
            print(f"Warning: Language '{target_language}' not supported by DeepL. Returning original text.")
            return text

        result = translator.translate_text(text, target_lang=target_language)
        return result.text
        
    except deepl.DeepLException as e:
        # In a real application, you would log this error.
        print(f"An error occurred with the DeepL API: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
