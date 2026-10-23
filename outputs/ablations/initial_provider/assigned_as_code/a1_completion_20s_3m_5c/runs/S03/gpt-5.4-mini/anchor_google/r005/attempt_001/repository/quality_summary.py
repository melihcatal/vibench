from google.cloud import language_v1


def quality_summary(payload, config=None):
    client = language_v1.LanguageServiceClient()
    text = payload["text"]
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(request={"document": document})
    return {
        "score": sentiment.document_sentiment.score,
        "magnitude": sentiment.document_sentiment.magnitude,
        "issues": ["low_sentiment"] if sentiment.document_sentiment.score < -0.25 else [],
    }
