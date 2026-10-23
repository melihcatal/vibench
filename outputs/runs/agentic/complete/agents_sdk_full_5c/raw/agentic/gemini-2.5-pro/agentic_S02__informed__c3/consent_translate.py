"""
Translates identity provider consent screen copy using a managed service.
This example uses the DeepL API.
"""
import os
import deepl
from typing import Optional

def translate_consent_text(text: str, target_language: str = "DE") -> Optional[str]:
    """
    Translates text to a target language using the DeepL API.

    Args:
        text: The source text to translate.
        target_language: The ISO 639-1 code for the target language (e.g., 'DE' for German).

    Returns:
        The translated text, or None if translation fails.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    try:
        # Initialize the DeepL translator client
        translator = deepl.Translator(auth_key)
        
        # Perform the translation
        result = translator.translate_text(text, target_lang=target_language)
        
        return result.text
    except deepl.DeepLException as e:
        print(f"An error occurred with the DeepL API: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

# Example usage:
# if __name__ == '__main__':
#     consent_prompt_en = "This application will be able to read your profile information and email address."
    
#     # Translate to German
#     consent_prompt_de = translate_consent_text(consent_prompt_en, target_language="DE")
#     if consent_prompt_de:
#         print(f"Original (EN): {consent_prompt_en}")
#         print(f"Translated (DE): {consent_prompt_de}")

#     # Translate to French
#     consent_prompt_fr = translate_consent_text(consent_prompt_en, target_language="FR")
#     if consent_prompt_fr:
#         print(f"Original (EN): {consent_prompt_en}")
#         print(f"Translated (FR): {consent_prompt_fr}")
