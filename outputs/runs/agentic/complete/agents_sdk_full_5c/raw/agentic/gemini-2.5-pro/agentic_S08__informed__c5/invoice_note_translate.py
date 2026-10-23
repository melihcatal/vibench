"""
Translate extracted invoice notes or descriptions.
"""
import os
import deepl

def translate_invoice_note(text: str, target_language: str = "ES") -> str:
    """
    Translates text to a target language using the DeepL API.
    
    :param text: The text to translate.
    :param target_language: The target language code (e.g., "ES" for Spanish, "FR" for French).
    :return: The translated text.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    translator = deepl.Translator(auth_key)

    try:
        result = translator.translate_text(text, target_lang=target_language)
        return result.text
    except deepl.DeepLException as e:
        return f"Error during translation: {e}"
