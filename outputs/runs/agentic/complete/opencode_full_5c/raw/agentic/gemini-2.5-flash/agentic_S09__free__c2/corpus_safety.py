from google.cloud import language_v1
import os


def check_text_safety(text: str) -> dict:
    # Google Cloud Natural Language API client
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set for authentication
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    # Detect sentiment for a basic safety check (e.g., highly negative sentiment might flag as unsafe)
    sentiment = client.analyze_sentiment(
        request={"document": document}
    ).document_sentiment

    # You could expand this with more sophisticated checks, e.g., custom content moderation API
    is_safe = True
    safety_score = (
        sentiment.score + 1
    ) / 2  # Normalize sentiment score from [-1, 1] to [0, 1]

    if sentiment.score < -0.7:  # Example threshold for very negative content
        is_safe = False

    return {
        "text": text,
        "is_safe": is_safe,
        "sentiment_score": sentiment.score,
        "sentiment_magnitude": sentiment.magnitude,
        "provider": "Google Cloud Natural Language API",
    }
