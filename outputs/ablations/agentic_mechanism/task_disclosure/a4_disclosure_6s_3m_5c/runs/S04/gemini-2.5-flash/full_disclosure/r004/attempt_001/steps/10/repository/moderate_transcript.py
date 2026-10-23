from google.cloud import language_v1

def moderate_transcript(text: str):
    """
    Moderates transcript text using Google Cloud Natural Language API.

    Args:
        text: The transcript text to moderate.

    Returns:
        A dictionary containing moderation results (e.g., sentiment score, categories).
    """
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment

    moderation_result = {
        "sentiment_score": sentiment.score,
        "sentiment_magnitude": sentiment.magnitude,
    }

    return moderation_result
