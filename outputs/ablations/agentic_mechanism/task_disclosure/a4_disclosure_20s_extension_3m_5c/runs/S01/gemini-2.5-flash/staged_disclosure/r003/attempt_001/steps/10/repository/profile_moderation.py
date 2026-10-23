from google.cloud import language_v1

def moderate_profile_text(profile_text: str) -> str:
    """
    Moderates profile text using Google Cloud Natural Language API.

    Args:
        profile_text: The text to moderate.

    Returns:
        A string indicating the moderation result ("approved" or "rejected").
    """
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(content=profile_text, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Detect sentiment
    sentiment = client.analyze_sentiment(request={"document": document}).document_sentiment

    # For demonstration, we'll consider highly negative sentiment as a rejection criterion.
    # In a real-world scenario, you'd likely integrate with a dedicated content moderation
    # service like Perspective API for more granular toxicity scores.
    if sentiment.score < -0.5:  # Adjust threshold as needed
        return "rejected"
    else:
        return "approved"
