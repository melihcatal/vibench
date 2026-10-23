from google.cloud import language_v1

from document_models import TextResponse


def check_ocr_safety(text_response: TextResponse) -> dict:
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=text_response.text, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    analysis = client.analyze_sentiment(request={"document": document})
    return {
        "score": analysis.document_sentiment.score,
        "magnitude": analysis.document_sentiment.magnitude,
    }
