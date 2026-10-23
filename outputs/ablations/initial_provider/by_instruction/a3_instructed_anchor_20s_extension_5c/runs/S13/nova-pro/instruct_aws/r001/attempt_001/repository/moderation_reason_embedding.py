from safety_client import get_comprehend_client
from safety_models import SafetyRequest, SafetyResponse, normalize_response

def moderation_reason_embedding(text):
    client = get_comprehend_client()
    request = SafetyRequest(text)
    response = client.detect_sentiment(Text=request.text, LanguageCode='en')
    return response['Sentiment']