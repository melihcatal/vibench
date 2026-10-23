from google.cloud import language_v1


def archive_summary(payload, config=None):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=payload["text"], type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(request={"document": document})
    return {
        "status": "COMPLETED",
        "summary": payload["text"][:280],
        "sentiment_score": response.document_sentiment.score,
    }
