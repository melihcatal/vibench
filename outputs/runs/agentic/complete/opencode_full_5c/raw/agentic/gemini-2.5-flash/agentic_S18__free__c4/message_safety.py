from google.cloud import language_v1


def check_message_safety(text_content: str) -> dict:
    """Checks message payload text for safety using Google Cloud Natural Language API.

    This function performs sentiment analysis as a proxy for content safety.
    Highly negative sentiment might indicate potentially unsafe or toxic content.

    Args:
        text_content: The text content from the message payload to check.

    Returns:
        A dictionary with sentiment score, magnitude, and a safety prediction.
    """
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    sentiment = client.analyze_sentiment(
        request={"document": document}
    ).document_sentiment

    # A simple heuristic: if score is very negative and magnitude is high, it might be unsafe.
    # Thresholds can be adjusted based on specific safety requirements.
    is_unsafe = sentiment.score < -0.5 and sentiment.magnitude > 1.0

    return {
        "text": text_content,
        "sentiment_score": sentiment.score,
        "sentiment_magnitude": sentiment.magnitude,
        "is_potentially_unsafe": is_unsafe,
        "provider": "Google Cloud Natural Language API",
    }
