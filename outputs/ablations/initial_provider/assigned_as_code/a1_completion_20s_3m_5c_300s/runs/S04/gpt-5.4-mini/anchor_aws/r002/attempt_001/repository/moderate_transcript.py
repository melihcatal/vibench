from google.cloud import language_v1


def moderate_transcript(payload, config=None):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=payload["text"], type_=language_v1.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(request={"document": document})
    return {
        "approved": sentiment.document_sentiment.score >= (config or {}).get("threshold", 0.0),
        "score": sentiment.document_sentiment.score,
    }
