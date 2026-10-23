import deepl
from document_client import get_deepl_translator

def translate_invoice_note(
    text: str, target_lang: str = "EN-US"
) -> str:
    """
    Translates a piece of text to the specified target language using DeepL API.

    Args:
        text: The text to be translated.
        target_lang: The target language code (e.g., "EN-US", "DE", "FR").

    Returns:
        The translated text as a string.
    """
    if not text:
        return ""

    try:
        translator = get_deepl_translator()
        result = translator.translate_text(text, target_lang=target_lang)
        return result.text
    except deepl.DeepLException as e:
        # Handle potential API errors, e.g., authentication failure or invalid language
        print(f"DeepL API error: {e}")
        return f"Error during translation: {e}"

