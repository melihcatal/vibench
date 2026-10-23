from google.cloud import language_v1

def check_unsafe_text(text: str) -> dict:
    """
    Checks the input text for unsafe content using Google Cloud Natural Language API.

    Args:
        text: The text to be analyzed.

    Returns:
        A dictionary containing the analysis results.
    """
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Perform sentiment analysis to get a general idea. More sophisticated content moderation
    # would involve entity analysis or custom classification models.
    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment

    # For demonstration, we'll consider very negative sentiment as potentially "unsafe"
    # in a broader sense, though true content moderation is more complex.
    is_unsafe = sentiment.score < -0.5

    return {
        "text": text,
        "sentiment_score": sentiment.score,
        "sentiment_magnitude": sentiment.magnitude,
        "is_potentially_unsafe": is_unsafe,
        "provider": "Google Cloud Natural Language API"
    }
