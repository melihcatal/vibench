from google.cloud import language_v1 as language

from document_models import OCRRequest
from extract_text import extract_text


def ocr_safety(request: OCRRequest) -> dict:
    source = extract_text(request)
    client = language.LanguageServiceClient()
    document = language.Document(content=source.text, type_=language.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(request={"document": document})
    return {"provider": "google_cloud_natural_language", "score": sentiment.document_sentiment.score, "text": source.text}
