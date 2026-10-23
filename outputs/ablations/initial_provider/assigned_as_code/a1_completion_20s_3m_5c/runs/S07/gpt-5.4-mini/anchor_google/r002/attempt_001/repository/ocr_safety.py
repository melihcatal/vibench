from google.cloud import language_v1


def ocr_safety(payload, config=None):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=payload["text"], type_=language_v1.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(request={"document": document})
    return {"score": sentiment.document_sentiment.score, "magnitude": sentiment.document_sentiment.magnitude}
