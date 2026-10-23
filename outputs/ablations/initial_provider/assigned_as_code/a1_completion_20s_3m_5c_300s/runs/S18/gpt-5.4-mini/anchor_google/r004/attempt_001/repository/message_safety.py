from google.cloud import language_v1


def message_safety(payload, config=None):
    client = language_v1.LanguageServiceClient()
    text = payload.get("text", "") if isinstance(payload, dict) else str(payload)
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(request={"document": document})
    return {"unsafe": response.document_sentiment.score < -0.25, "score": response.document_sentiment.score}
