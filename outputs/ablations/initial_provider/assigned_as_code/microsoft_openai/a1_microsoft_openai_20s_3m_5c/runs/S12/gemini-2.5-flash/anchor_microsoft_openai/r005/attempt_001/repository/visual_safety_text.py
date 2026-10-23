from google.cloud import language_v1
from vision_client import get_language_client
from vision_models import TextSafetyRequest, TextSafetyResponse

def visual_safety_text(payload: TextSafetyRequest, config: dict = None) -> TextSafetyResponse:
    client = get_language_client()

    document = language_v1.Document(content=payload.text, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Analyze sentiment
    sentiment_response = client.analyze_sentiment(request={'document': document})
    sentiment = sentiment_response.document_sentiment

    # Classify text content
    classification_response = client.classify_text(request={'document': document})
    categories = [{'name': category.name, 'confidence': category.confidence}
                  for category in classification_response.categories]

    return TextSafetyResponse(
        sentiment_score=sentiment.score,
        sentiment_magnitude=sentiment.magnitude,
        categories=categories
    )
