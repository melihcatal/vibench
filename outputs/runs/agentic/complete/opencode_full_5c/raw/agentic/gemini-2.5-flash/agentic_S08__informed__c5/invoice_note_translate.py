from document_client import get_google_cloud_translate_client


def translate_invoice_notes(text: str, target_language: str = "en") -> str:
    translate_client = get_google_cloud_translate_client()
    response = translate_client.translate(text, target_language=target_language)
    return response["translatedText"]
