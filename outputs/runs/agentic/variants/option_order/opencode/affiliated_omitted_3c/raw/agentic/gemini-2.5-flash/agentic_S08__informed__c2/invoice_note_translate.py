from document_client import get_translation_client
from azure.ai.translation.text.models import InputTextItem


def translate_invoice_note(text: str, target_language: str = "en") -> str:
    client = get_translation_client()

    if not text:
        return ""

    request_body = [InputTextItem(text=text)]
    response = client.translate(body=request_body, to=[target_language])

    translated_text = ""
    if response and response[0].translations:
        translated_text = response[0].translations[0].text

    return translated_text
