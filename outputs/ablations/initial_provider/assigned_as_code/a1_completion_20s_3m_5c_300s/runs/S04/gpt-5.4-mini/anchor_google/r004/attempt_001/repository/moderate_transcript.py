from google.cloud import language_v1


def moderate_transcript(payload, config=None):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=payload["text"], type_=language_v1.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(request={"document": document}).document_sentiment
    return {"label": "OK" if sentiment.score >= 0 else "REVIEW", "score": sentiment.score, "magnitude": sentiment.magnitude}
