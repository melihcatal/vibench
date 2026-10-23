from google.cloud import language_v1

from document_models import OCRResponse, SafetyResponse


def check_ocr_safety(ocr: OCRResponse) -> SafetyResponse:
    client = language_v1.LanguageServiceClient()
    doc = language_v1.Document(content=ocr.text, type_=language_v1.Document.Type.PLAIN_TEXT)
    annotations = client.analyze_sentiment(request={"document": doc})
    score = annotations.document_sentiment.score if annotations.document_sentiment else 0.0
    safe = score >= -0.25
    return SafetyResponse(safe=safe, categories={"sentiment_score": score}, raw=annotations)
