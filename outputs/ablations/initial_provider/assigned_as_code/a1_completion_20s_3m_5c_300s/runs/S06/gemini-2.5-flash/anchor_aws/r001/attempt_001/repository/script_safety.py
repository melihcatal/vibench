from google.cloud import language_v1
import os


def script_safety(payload, config=None):
    config = config or {}
    client = language_v1.LanguageServiceClient()

    text_content = payload.get("text")
    if not text_content:
        raise ValueError("Text content not provided in payload.")

    document = language_v1.Document(content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Perform sentiment analysis to get a general idea, can be extended with custom content classification
    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment
    
    # For more robust safety checks, one would typically use a dedicated content moderation API or custom classification
    # Here, we'll provide a basic indicator based on sentiment score
    is_safe = True
    safety_score = sentiment.score # -1 to 1, higher is more positive

    if safety_score < -0.5:
        is_safe = False # Potentially negative or unsafe content

    return {"is_safe": is_safe, "sentiment_score": sentiment.score, "sentiment_magnitude": sentiment.magnitude}
