import os
import deepl

def translate_dashboard_note(note_text: str, target_language_code: str = "JA") -> str:
    """
    Translates metric or dashboard notes for another locale using the DeepL API.

    Args:
        note_text: The text to be translated.
        target_language_code: The target language code (e.g., "DE", "FR", "JA").

    Returns:
        The translated text.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    translator = deepl.Translator(auth_key)

    try:
        result = translator.translate_text(note_text, target_lang=target_language_code)
        return result.text
    except deepl.DeepLException as e:
        # Handle API errors
        return f"Error during translation: {str(e)}"
