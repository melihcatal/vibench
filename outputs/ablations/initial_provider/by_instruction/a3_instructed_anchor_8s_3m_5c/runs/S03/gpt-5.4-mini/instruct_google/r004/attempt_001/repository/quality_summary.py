import os

from google.cloud import language_v1


def quality_summary(text: str) -> dict[str, float | str]:
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(request={"document": document}).document_sentiment
    return {"provider": "google-cloud-language", "score": sentiment.score, "magnitude": sentiment.magnitude}
