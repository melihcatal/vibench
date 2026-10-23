import os
import deepl

def translate_compliance_note(text: str, target_lang: str = "DE") -> str:
    """
    Translates an encryption or compliance note for reviewers using the DeepL API.
    
    Args:
        text: The text to be translated.
        target_lang: The target language code (e.g., "DE" for German, "FR" for French).

    Returns:
        The translated text.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    try:
        translator = deepl.Translator(auth_key)
        result = translator.translate_text(text, target_lang=target_lang)
        return result.text
    except deepl.DeepLException as e:
        return f"An error occurred during translation: {e}"
