import deepl
from security_client import get_deepl_translator

def translate_note_with_deepl(
    note: str,
    target_lang: str = "DE"
) -> str:
    """
    Translates a compliance note to a target language using DeepL.

    Args:
        note: The text of the note to translate.
        target_lang: The target language code (e.g., 'DE' for German).

    Returns:
        The translated text.
    """
    translator = get_deepl_translator()
    try:
        # Provider-specific call to DeepL API
        result = translator.translate_text(note, target_lang=target_lang)
        return result.text
    except deepl.DeepLException as e:
        return f"Error during translation with DeepL: {e}"
