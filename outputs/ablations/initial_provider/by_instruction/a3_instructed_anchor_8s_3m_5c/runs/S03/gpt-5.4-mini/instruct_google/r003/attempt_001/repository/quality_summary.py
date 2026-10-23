from google.cloud import language_v1

from translation_models import normalize_text


def quality_summary(text: str) -> dict:
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=normalize_text(text), type_=language_v1.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(request={"document": document}).document_sentiment
    return {"provider": "google", "score": sentiment.score, "magnitude": sentiment.magnitude}
