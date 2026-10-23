from google.cloud import translate_v3

from security_models import normalize_label_text


def runbook_translate(text: str, target_language_code: str = "es") -> str:
    client = translate_v3.TranslationServiceClient()
    cleaned = normalize_label_text(text)
    parent = "projects/0/locations/global"
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [cleaned],
            "mime_type": "text/plain",
            "target_language_code": target_language_code,
        }
    )
    return response.translations[0].translated_text
