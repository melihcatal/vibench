from safety_client import comprehend
from safety_models import SafetyRequest, SafetyResponse, normalize_response


def redact_unsafe(text):
    request = SafetyRequest(text)
    response = comprehend.detect_sentiment(Text=request.text, LanguageCode="en")
    if response["Sentiment"] == "NEGATIVE":
        return "[REDACTED]"
    return text
