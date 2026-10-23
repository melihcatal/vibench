from google.cloud import language_v1


def moderate_batch(texts: list[str]) -> list[dict]:
    """Moderates a batch of user messages using Google Cloud Natural Language API."""
    client = language_v1.LanguageServiceClient()
    results = []
    for text in texts:
        document = language_v1.Document(
            content=text, type_=language_v1.Document.Type.PLAIN_TEXT
        )
        response = client.analyze_sentiment(document=document)
        results.append(
            {
                "text": text,
                "sentiment_score": response.document_sentiment.score,
                "sentiment_magnitude": response.document_sentiment.magnitude,
            }
        )
    return results
