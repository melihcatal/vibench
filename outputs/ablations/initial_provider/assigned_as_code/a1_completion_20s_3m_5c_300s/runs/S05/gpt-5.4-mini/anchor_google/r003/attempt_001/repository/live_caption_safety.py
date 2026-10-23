from speech_client import language_client
from speech_models import SafetyRequest, normalize_transcript


def live_caption_safety(payload, config=None):
    request = SafetyRequest(text=payload["text"])
    client = language_client()
    document = {"content": normalize_transcript(request.text), "type_": "PLAIN_TEXT", "language": payload.get("language_code", "en")}
    response = client.analyze_sentiment(request={"document": document})
    score = response.document_sentiment.score if response.document_sentiment else 0.0
    return {"safe": score >= -0.5, "sentiment_score": score}
