from google.cloud import language_v1


def visual_safety_text(payload, config=None):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=payload["text"], type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(request={"document": document})
    return {"score": response.document_sentiment.score, "magnitude": response.document_sentiment.magnitude}
