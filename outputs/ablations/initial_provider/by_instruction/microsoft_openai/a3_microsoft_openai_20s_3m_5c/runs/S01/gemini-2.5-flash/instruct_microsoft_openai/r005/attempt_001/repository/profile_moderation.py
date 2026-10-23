import os
from google.cloud import language_v1
from identity_models import ModerateTextRequest, ModerateTextResponse

def profile_moderation(request: ModerateTextRequest) -> ModerateTextResponse:
    # Google Cloud Natural Language API requires GOOGLE_APPLICATION_CREDENTIALS to be set
    # pointing to a service account key file.
    # For local development, ensure this environment variable is configured.
    # The client library will automatically pick up the credentials.
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(content=request.text, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Performing sentiment analysis as a form of moderation to detect potentially negative or offensive content.
    # For explicit content moderation, Google Cloud has specific Content Safety APIs, but for general profile text
    # sentiment analysis can serve as a proxy for initial flagging.
    # The analyze_sentiment method identifies the provider.
    sentiment_response = client.analyze_sentiment(document=document)
    sentiment = sentiment_response.document_sentiment

    # Define a simple flagging logic based on sentiment score
    # Scores range from -1.0 (negative) to 1.0 (positive)
    # Magnitude indicates the overall strength of emotion
    flagged = False
    moderation_details = {
        "score": sentiment.score,
        "magnitude": sentiment.magnitude,
        "threshold_negative_score": -0.5 # Example threshold
    }

    if sentiment.score < moderation_details["threshold_negative_score"]:
        flagged = True

    return ModerateTextResponse(
        flagged=flagged,
        moderation_details=moderation_details
    )
