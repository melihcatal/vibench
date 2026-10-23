from google.cloud import language_v1
import os


def check_text_safety(text_content: str) -> dict:
    """Checks user-generated document fields for unsafe content using Google Cloud Natural Language API."""
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    # Perform sentiment analysis as a proxy for safety (can be expanded with content classification)
    response = client.analyze_sentiment(document=document)
    sentiment = response.document_sentiment

    # For more robust safety, you would typically use a dedicated content moderation API
    # or analyze entities and categories.

    return {
        "score": sentiment.score,
        "magnitude": sentiment.magnitude,
        "is_safe": sentiment.score
        >= -0.1,  # Example threshold, customize based on needs
    }
