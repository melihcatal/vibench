from document_client import DocumentClients

def translate_invoice_note(text: str, target_language: str = "en") -> str:
    clients = DocumentClients()
    if not clients.google_translate_client:
        raise ValueError("Google Cloud Translation client not initialized.")

    if not text:
        return ""

    result = clients.google_translate_client.translate(text, target_language=target_language)
    return result["translatedText"]
