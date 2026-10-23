import os
from google.cloud import language_v1


def moderate_text_claim(text: str) -> dict:
    # Instantiates a client
    client = language_v1.LanguageServiceClient()

    # The text to analyze
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Detects the sentiment of the text
    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment

    # Detects categories in the text
    # Note: Categorization requires a larger text. For short claims, it might not return much.
    # response = client.classify_text(request={'document': document})
    # categories = [category.name for category in response.categories]

    # Placeholder for content moderation. GCP Natural Language API doesn't have a direct
    # "moderation" score like some other services. We can infer based on sentiment.
    # For direct content moderation, Google Cloud has the "Perspective API" (not part of NL API)
    # or specific AI Platform models.

    is_negative = sentiment.score < -0.2  # Threshold for considering sentiment negative

    return {
        "text": text,
        "sentiment_score": sentiment.score,
        "sentiment_magnitude": sentiment.magnitude,
        "moderation_flagged": is_negative, # Simple flagging based on sentiment
        "moderation_notes": "Flagged due to negative sentiment" if is_negative else ""
    }
