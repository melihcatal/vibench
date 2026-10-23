from safety_client import comprehend
from safety_models import SafetyRequest, SafetyResponse, normalize_response


def safety_threshold(text, threshold=0.5):
    request = SafetyRequest(text)
    response = comprehend.detect_sentiment(Text=request.text, LanguageCode="en")
    sentiment_score = response["SentimentScore"]["Negative"]
    return sentiment_score > threshold
