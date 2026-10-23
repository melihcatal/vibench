from document_client import get_translate_client

def translate_invoice_note(text: str, target_language: str = "en") -> str:
    client = get_translate_client()
    response = client.translate(text, target_language=target_language)
    return response["translatedText"]
