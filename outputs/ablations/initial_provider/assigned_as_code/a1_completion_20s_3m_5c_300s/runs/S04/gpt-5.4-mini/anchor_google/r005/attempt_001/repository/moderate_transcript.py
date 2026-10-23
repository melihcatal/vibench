from google.cloud import language_v1

from speech_models import normalize_transcript


def moderate_transcript(payload, config=None):
    config = config or {}
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=normalize_transcript(payload), type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(request={"document": document})
    return {"sentiment_score": response.document_sentiment.score, "sentiment_magnitude": response.document_sentiment.magnitude, "approved": response.document_sentiment.score >= config.get("min_sentiment_score", -0.25)}
