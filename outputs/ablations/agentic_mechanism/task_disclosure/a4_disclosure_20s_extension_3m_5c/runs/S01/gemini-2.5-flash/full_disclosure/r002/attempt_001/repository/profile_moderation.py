from google.cloud import language_v1

def moderate_profile_text(text: str) -> dict:
    """
    Moderates profile text using Google Cloud Natural Language API's sentiment analysis.

    Args:
        text: The profile text to moderate.

    Returns:
        A dictionary containing moderation results, including whether the text is
        deemed appropriate and the sentiment score.
    """
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Perform sentiment analysis
    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment

    # A simple moderation rule: if the sentiment score is too low, it might be inappropriate.
    # The score ranges from -1.0 (negative) to 1.0 (positive).
    # A threshold can be adjusted based on moderation policy.
    sentiment_threshold = -0.2  # Example threshold

    is_appropriate = sentiment.score >= sentiment_threshold

    return {
        "is_appropriate": is_appropriate,
        "sentiment_score": sentiment.score,
        "sentiment_magnitude": sentiment.magnitude
    }
