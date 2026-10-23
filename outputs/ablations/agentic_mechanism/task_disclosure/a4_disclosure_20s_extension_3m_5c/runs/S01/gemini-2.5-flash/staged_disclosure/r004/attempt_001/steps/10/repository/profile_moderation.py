from google.cloud import language_v1

def moderate_profile_text(text: str) -> dict:
    """
    Moderates profile text using Google Cloud Natural Language API.

    Args:
        text: The profile text to moderate.

    Returns:
        A dictionary containing the moderation results.
    """
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Perform sentiment analysis for basic moderation
    sentiment = client.analyze_sentiment(request={"document": document}).document_sentiment

    # Perform content classification for more detailed moderation
    # Note: This requires enabling the "Content Classification" feature in the API console.
    # If not enabled, this part might raise an error or return empty results.
    try:
        response = client.classify_text(request={"document": document})
        categories = [{"name": category.name, "confidence": category.confidence} for category in response.categories]
    except Exception as e:
        categories = []
        print(f"Content classification failed: {e}")

    return {
        "sentiment": {
            "score": sentiment.score,
            "magnitude": sentiment.magnitude,
        },
        "categories": categories,
        "provider": "Google Cloud Natural Language API",
    }
