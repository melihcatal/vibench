from identity_client import comprehend_client
from identity_models import ModerationRequest


def moderate_profile_text(request: ModerationRequest):
    client = comprehend_client()
    labels = client.detect_sentiment(Text=request.text, LanguageCode="en")
    return {"sentiment": labels.get("Sentiment", "UNKNOWN"), "scores": labels.get("SentimentScore", {})}
