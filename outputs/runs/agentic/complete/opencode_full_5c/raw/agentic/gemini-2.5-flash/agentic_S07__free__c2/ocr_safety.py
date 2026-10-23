from document_client import get_language_client
from google.cloud import language_v2


def check_text_safety(text: str) -> dict:
    client = get_language_client()

    document = language_v2.Document(
        content=text, type_=language_v2.Document.Type.PLAIN_TEXT
    )

    # Classify text to check for general content categories
    # Note: This is a general classification and not a dedicated 'safety' API like Perspective API.
    # For robust safety checks, consider integrating with a specialized content moderation API.
    response = client.classify_text(document=document)

    categories = []
    for category in response.categories:
        categories.append({"name": category.name, "confidence": category.confidence})

    # As a basic safety indicator, we can also look at sentiment.
    # More advanced safety requires a dedicated content moderation service.
    sentiment_response = client.analyze_sentiment(document=document)
    sentiment = {
        "score": sentiment_response.document_sentiment.score,
        "magnitude": sentiment_response.document_sentiment.magnitude,
    }

    return {"categories": categories, "sentiment": sentiment}
