from google.cloud import language_v1

from document_models import extract_content, normalize_payload


def ocr_safety(payload, config=None):
    payload = normalize_payload(payload)
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=extract_content(payload), type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.moderate_text(request={'document': document})
    return {'unsafe': bool(getattr(response, 'moderation_categories', []))}
