import os
import deepl

def translate_dashboard_note(text: str, target_language: str = "DE") -> str:
    """
    Translates metric or dashboard notes for another locale using DeepL.

    :param text: The text to translate.
    :param target_language: The target language code (e.g., "DE", "FR", "ES").
    :return: The translated text.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    translator = deepl.Translator(auth_key)

    try:
        result = translator.translate_text(text, target_lang=target_language)
        return result.text
    except deepl.DeepLException as e:
        return f"An error occurred during translation: {e}"
