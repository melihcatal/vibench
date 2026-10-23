# invoice_note_translate.py
from document_client import get_deepl_translator

def translate_invoice_note(
    note: str,
    target_lang: str = "EN-US"
) -> str:
    """
    Translates an invoice note to a target language using the DeepL API.
    
    :param note: The text to translate.
    :param target_lang: The target language code (e.g., "EN-US", "DE", "FR").
    :return: The translated text.
    """
    translator = get_deepl_translator()
    result = translator.translate_text(note, target_lang=target_lang)
    return result.text
