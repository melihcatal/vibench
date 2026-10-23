from __future__ import annotations

from google.cloud import language_v1


def check_log_text_safety(text: str) -> bool:
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(request={"document": document})
    return response.document_sentiment.score >= -0.5
