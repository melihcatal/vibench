import os
from google.cloud import language_v1


def check_text_safety(text, categories=None):
    """Check narration scripts for unsafe content using Google Cloud Natural Language API."""
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    if categories:
        request = language_v1.AnalyzeEntitySentimentRequest(
            document=document, encoding_type=language_v1.EncodingType.UTF8
        )
        response = client.analyze_entity_sentiment(request=request)

        unsafe_entities = []
        for entity in response.entities:
            if entity.sentiment.score < -0.5:
                unsafe_entities.append(
                    {
                        "name": entity.name,
                        "type": language_v1.Entity.Type(entity.type_).name,
                        "sentiment_score": entity.sentiment.score,
                        "sentiment_magnitude": entity.sentiment.magnitude,
                    }
                )

        return {
            "is_safe": len(unsafe_entities) == 0,
            "unsafe_entities": unsafe_entities,
            "text_length": len(text),
        }
    else:
        request = language_v1.AnalyzeSentimentRequest(
            document=document, encoding_type=language_v1.EncodingType.UTF8
        )
        response = client.analyze_sentiment(request=request)

        document_sentiment = response.document_sentiment

        is_safe = document_sentiment.score >= -0.3

        return {
            "is_safe": is_safe,
            "sentiment_score": document_sentiment.score,
            "sentiment_magnitude": document_sentiment.magnitude,
            "text_length": len(text),
        }


def moderate_text(text):
    """Moderate text for inappropriate content."""
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    request = language_v1.ClassifyTextRequest(document=document)

    try:
        response = client.classify_text(request=request)

        categories = []
        for category in response.categories:
            categories.append(
                {"name": category.name, "confidence": category.confidence}
            )

        has_inappropriate = any(
            "adult" in cat["name"].lower()
            or "violence" in cat["name"].lower()
            or "toxic" in cat["name"].lower()
            for cat in categories
        )

        return {
            "is_appropriate": not has_inappropriate,
            "categories": categories,
            "text_length": len(text),
        }
    except Exception as e:
        return {"is_appropriate": True, "error": str(e), "text_length": len(text)}
