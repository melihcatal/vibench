from safety_client import comprehend
from safety_models import SafetyRequest, SafetyResponse, normalize_response


def moderate_batch(texts):
    decisions = []
    for text in texts:
        request = SafetyRequest(text)
        response = comprehend.detect_sentiment(Text=request.text, LanguageCode="en")
        decisions.append(normalize_response(response))
    return decisions
