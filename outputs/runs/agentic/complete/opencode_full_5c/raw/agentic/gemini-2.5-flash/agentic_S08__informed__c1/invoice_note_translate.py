from document_client import get_google_translate_client
from google.cloud import translate_v2 as translate


def translate_invoice_notes(text: str, target_language: str = "en") -> str:
    translate_client: translate.Client = get_google_translate_client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    # Target language can be specified, defaulting to English
    result = translate_client.translate(text, target_language=target_language)

    return result["translatedText"]
