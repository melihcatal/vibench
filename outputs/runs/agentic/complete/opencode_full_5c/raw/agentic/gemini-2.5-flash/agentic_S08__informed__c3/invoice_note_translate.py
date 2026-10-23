import deepl
from document_client import get_deepl_translator


def translate_invoice_note(text: str, target_lang: str = "en") -> str:
    translator = get_deepl_translator()

    try:
        result = translator.translate_text(text, target_lang=target_lang)
        return result.text
    except deepl.exceptions.DeepLException as e:
        return f"Translation error: {e}"
