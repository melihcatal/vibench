from google.cloud import language_v1


def message_safety(payload, config=None):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=payload["text"], type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(request={"document": document})
    score = response.document_sentiment.score
    return {"safe": score >= -0.2, "score": score}
