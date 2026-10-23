from google.cloud import language_v1

def check_text_for_safety(text: str) -> bool:
    """
    Checks the given text for safety using Google Cloud Natural Language API.
    Returns True if the text is considered safe, False otherwise.
    """
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Perform sentiment analysis as a basic safety check.
    # More advanced safety checks would involve content classification or custom models.
    response = client.analyze_sentiment(document=document)
    sentiment_score = response.document_sentiment.score

    # A very low (negative) sentiment score might indicate unsafe content.
    # The threshold here is arbitrary and can be adjusted based on requirements.
    # For a real-world application, consider using content classification APIs
    # like the Perspective API or custom machine learning models for safety.
    if sentiment_score < -0.5:  # Example threshold
        return False
    return True
