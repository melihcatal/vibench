from google.cloud import language_v1

def check_caption_safety(text: str):
    """Checks live transcript text for unsafe content using Google Cloud Natural Language API.

    This function performs sentiment analysis as a proxy for safety. A more robust safety
    check would involve content moderation APIs or custom models.

    Args:
        text: The live transcript text to check.

    Returns:
        A dictionary containing sentiment score and magnitude.
    """
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment

    # Interpret sentiment score:
    #   - score > 0.25: positive
    #   - score < -0.25: negative
    #   - -0.25 <= score <= 0.25: neutral

    # Interpret magnitude:
    #   - Indicates the overall strength of emotion (positive or negative) in the document.
    #   - Documents with a higher magnitude are more emotional.

    return {
        "score": sentiment.score,
        "magnitude": sentiment.magnitude,
        "sentiment_category": (
            "positive" if sentiment.score > 0.25 else
            "negative" if sentiment.score < -0.25 else
            "neutral"
        )
    }
