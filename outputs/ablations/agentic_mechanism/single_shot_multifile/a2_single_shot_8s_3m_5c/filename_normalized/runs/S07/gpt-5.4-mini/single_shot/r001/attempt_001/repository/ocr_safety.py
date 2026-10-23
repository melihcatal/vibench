from google.cloud import language_v1
from document_models import OCRTextResponse


def check_ocr_text_safety(ocr_response: OCRTextResponse) -> dict:
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=ocr_response.text, type_=language_v1.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(request={"document": document})
    magnitude = getattr(sentiment.document_sentiment, "magnitude", 0.0)
    score = getattr(sentiment.document_sentiment, "score", 0.0)
    unsafe = score < -0.5 or magnitude > 1.5
    return {"unsafe": unsafe, "score": score, "magnitude": magnitude}
