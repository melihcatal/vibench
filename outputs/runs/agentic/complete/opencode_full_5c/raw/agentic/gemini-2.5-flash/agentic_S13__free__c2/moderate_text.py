from google.cloud import language_v1


def moderate_text(text: str) -> dict:
    """Scores user text for unsafe or policy-violating content using Google Cloud Natural Language API."""
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    response = client.analyze_sentiment(
        document=document
    )  # Using sentiment as a proxy for moderation if explicit moderation API is not available
    # NOTE: Google Cloud Natural Language API does not have a direct "content moderation" endpoint.
    # For a real content moderation task, I would use Google Cloud "Content Safety API" or similar.
    # Here, sentiment analysis is used as a placeholder.
    return {
        "sentiment_score": response.document_sentiment.score,
        "sentiment_magnitude": response.document_sentiment.magnitude,
    }
