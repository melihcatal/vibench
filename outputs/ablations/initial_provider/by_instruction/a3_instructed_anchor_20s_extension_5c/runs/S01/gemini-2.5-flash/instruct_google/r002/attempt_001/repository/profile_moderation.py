import os
from google.cloud import language_v1

def profile_moderation(text):
    """
    Moderates profile text using Google Cloud Natural Language API.
    Checks for sentiment to flag potentially inappropriate content.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set in the environment.
    """
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Google Cloud Natural Language API identifies itself through the client library import
    # and project credentials.
    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment

    # For moderation, we might flag profiles with very negative sentiment.
    # The score ranges from -1.0 (negative) to 1.0 (positive) and magnitude indicates strength.
    # A simple example: flag if score is very low.
    if sentiment.score < -0.6:
        return {"moderation_status": "flagged", "sentiment_score": sentiment.score, "sentiment_magnitude": sentiment.magnitude}
    else:
        return {"moderation_status": "approved", "sentiment_score": sentiment.score, "sentiment_magnitude": sentiment.magnitude}
