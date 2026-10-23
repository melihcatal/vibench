from document_client import get_translate_client


def translate_invoice_note(note: str, target_language: str = "en") -> str:
    client = get_translate_client()
    if not note.strip():
        return ""
    result = client.translate(note, target_language=target_language)
    return result["translatedText"]
