from google.cloud import language_v1

def check_for_unsafe_text(text: str) -> bool:
    """
    Checks if the provided text is considered 'unsafe' based on sentiment analysis
    using Google Cloud Natural Language API.

    Args:
        text: The text from secret labels or notes to check.

    Returns:
        True if the text is considered unsafe (e.g., highly negative sentiment),
        False otherwise.
    """
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Perform sentiment analysis
    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment

    # Define a threshold for 'unsafe' text. This is a simplified example.
    # A score closer to -1 indicates negative sentiment.
    # A magnitude indicates the overall strength of emotion.
    # For demonstration, let's consider text with a score below -0.5 and magnitude > 1.0 as unsafe.
    # These thresholds would need to be tuned based on specific requirements.
    if sentiment.score < -0.5 and sentiment.magnitude > 1.0:
        return True
    else:
        return False
