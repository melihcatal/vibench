from google.cloud import language_v1
import os

def moderate_profile_text(text: str):
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or authentication is handled appropriately for Google Cloud.
    # Example: os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/keyfile.json"

    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    # Perform sentiment analysis for a basic form of moderation
    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment

    # A simple moderation logic: if score is very negative, it might be problematic
    is_flagged = False
    if sentiment.score < -0.5:
        is_flagged = True

    return {
        "score": sentiment.score,
        "magnitude": sentiment.magnitude,
        "is_flagged": is_flagged
    }
