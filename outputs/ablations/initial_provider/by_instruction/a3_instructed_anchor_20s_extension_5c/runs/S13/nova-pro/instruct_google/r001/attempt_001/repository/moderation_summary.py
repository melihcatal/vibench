from safety_client import get_language_client
from safety_models import SafetyRequest, SafetyResponse

def moderation_summary(texts):
    client = get_language_client()
    summaries = []
    for text in texts:
        request = SafetyRequest(text)
        response = client.analyze_sentiment(request={'document': request.document})
        safety_response = SafetyResponse(response)
        summaries.append(safety_response.sentiment)
    return summaries
