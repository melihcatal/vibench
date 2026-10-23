import os
from google.cloud import language_v1

def record_text_safety(text_content: str) -> dict:
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set for authentication
    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        print("Warning: GOOGLE_APPLICATION_CREDENTIALS environment variable not set. Using default credentials.")

    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Perform sentiment analysis to get a general idea, can be extended for content classification
    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment

    # For more advanced safety checks, consider using the Moderation API or custom models
    # This example provides basic sentiment as a proxy for 'safety' for demonstration
    return {
        "score": sentiment.score,
        "magnitude": sentiment.magnitude,
        "is_safe": sentiment.score >= -0.2 # Simple heuristic: consider text 'safe' if sentiment is not strongly negative
    }
