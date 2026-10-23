from google.cloud import language_v1


def live_caption_safety(payload, config=None):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=payload["text"], type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(request={"document": document})
    score = response.document_sentiment.score if response.document_sentiment else 0.0
    unsafe = score < -0.6
    return {"text": payload["text"], "unsafe": unsafe, "score": score, "is_final": payload.get("is_final", False)}
