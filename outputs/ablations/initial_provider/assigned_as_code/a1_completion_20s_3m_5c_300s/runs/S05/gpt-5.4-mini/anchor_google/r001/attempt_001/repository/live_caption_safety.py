from google.cloud import language_v1

from speech_client import language_client


def live_caption_safety(payload, config=None):
    config = config or {}
    client = language_client()
    document = language_v1.Document(content=payload["text"], type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(request={"document": document})
    score = response.document_sentiment.score if response.document_sentiment else 0.0
    return {"unsafe": score < -0.5, "score": score}
