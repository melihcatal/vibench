from google.cloud import translate_v3 as translate

from database_models import DocumentResponse, normalize_document


def translate_record(record, target_language="en"):
    doc = normalize_document(record) or {}
    client = translate.TranslationServiceClient()
    parent = f"projects/{__import__('os').getenv('GOOGLE_CLOUD_PROJECT', 'demo')}/locations/global"
    text = doc.get("text") or doc.get("description") or ""
    if text:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "mime_type": "text/plain",
                "target_language_code": target_language,
            }
        )
        translated = (
            response.translations[0].translated_text if response.translations else text
        )
    else:
        translated = text
    return DocumentResponse(
        ok=True,
        data={"translated_text": translated, "document_id": doc.get("document_id")},
    ).__dict__


def handler(event, context=None):
    return translate_record(
        event.get("record", event), event.get("target_language", "en")
    )
