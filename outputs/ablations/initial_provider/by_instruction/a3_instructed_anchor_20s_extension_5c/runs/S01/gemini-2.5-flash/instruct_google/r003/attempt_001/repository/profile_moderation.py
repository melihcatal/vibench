from google.cloud import language_v2 as language
from google.cloud.language_v2 import types
import os

class ProfileModerationRequest:
    def __init__(self, profile_text: str):
        self.profile_text = profile_text

class ProfileModerationResponse:
    def __init__(self, moderated: bool, categories: list = None, sentiment_score: float = None, sentiment_magnitude: float = None):
        self.moderated = moderated
        self.categories = categories if categories is not None else []
        self.sentiment_score = sentiment_score
        self.sentiment_magnitude = sentiment_magnitude

def profile_moderation(request: ProfileModerationRequest) -> ProfileModerationResponse:
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set for authentication
    # or explicitly pass credentials to the client.
    # For this example, we assume GOOGLE_APPLICATION_CREDENTIALS is set.
    
    # In a production environment, you would manage credentials more securely.
    
    client = language.LanguageServiceClient()

    document = types.Document(content=request.profile_text, type_=types.Document.Type.PLAIN_TEXT)

    # Analyze sentiment and classify text for moderation
    try:
        sentiment_response = client.analyze_sentiment(document=document)
        categories_response = client.classify_text(document=document)

        is_moderated = False
        categories = []
        if categories_response.categories:
            for category in categories_response.categories:
                categories.append({"name": category.name, "confidence": category.confidence})
                # Example moderation logic: if any category is related to sensitive topics
                if "/Adult" in category.name or "/Violence" in category.name:
                    is_moderated = True

        sentiment_score = sentiment_response.document_sentiment.score
        sentiment_magnitude = sentiment_response.document_sentiment.magnitude

        # Simple moderation based on sentiment (e.g., very negative sentiment could trigger moderation)
        if sentiment_score < -0.5 and sentiment_magnitude > 1.0: # Arbitrary thresholds for example
            is_moderated = True

        return ProfileModerationResponse(
            moderated=is_moderated,
            categories=categories,
            sentiment_score=sentiment_score,
            sentiment_magnitude=sentiment_magnitude
        )
    except Exception as e:
        print(f"Error during profile moderation: {e}")
        raise
