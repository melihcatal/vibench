from google.cloud import language_v1

from document_models import normalize_text


def ocr_safety(payload, config=None):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=normalize_text(payload.get("text", "")), type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(request={"document": document})
    return {"score": response.document_sentiment.score, "magnitude": response.document_sentiment.magnitude}
