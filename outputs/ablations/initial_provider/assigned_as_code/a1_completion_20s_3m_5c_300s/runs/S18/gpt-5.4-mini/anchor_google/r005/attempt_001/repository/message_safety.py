from google.cloud import language_v1


def message_safety(payload, config=None):
    text = payload.get("text", "")
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(request={"document": document})
    score = response.document_sentiment.score if response.document_sentiment else 0.0
    return {"provider": "google_cloud_natural_language", "safe": score >= -0.25, "score": score}
