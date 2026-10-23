from google.cloud import language_v1

def moderate_profile_text(text: str) -> bool:
    """
    Moderates profile text using Google Cloud Natural Language API.

    Args:
        text: The profile text to moderate.

    Returns:
        True if the text is considered safe, False otherwise.
    """
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Perform sentiment analysis to get an idea of the text's overall tone.
    # For more robust content moderation, you would typically use content classification
    # or integrate with a dedicated content moderation service.
    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment

    # A simple example of moderation: if the sentiment score is very negative,
    # it might indicate inappropriate content. This is a basic illustration.
    # In a real-world scenario, you would use more sophisticated methods.
    if sentiment.score < -0.5:  # Arbitrary threshold for demonstration
        return False
    return True
