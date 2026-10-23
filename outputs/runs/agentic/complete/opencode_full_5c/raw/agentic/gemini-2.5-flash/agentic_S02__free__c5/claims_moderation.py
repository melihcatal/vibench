import os
from google.cloud import language_v1
from typing import Dict, Any, List


def moderate_text_claim(text_claim: str) -> Dict[str, Any]:
    """
    Moderates a free-text claim using Google Cloud Natural Language API to detect entities, sentiment, and categories.

    Args:
        text_claim: The free-text claim or note to moderate.

    Returns:
        A dictionary containing moderation results including sentiment, entities, and categories.
    """
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=text_claim, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    # Analyze Sentiment
    sentiment_response = client.analyze_sentiment(document=document)
    sentiment = {
        "score": sentiment_response.document_sentiment.score,
        "magnitude": sentiment_response.document_sentiment.magnitude,
    }

    # Analyze Entities
    entity_response = client.analyze_entities(
        document=document, encoding_type=language_v1.EncodingType.UTF8
    )
    entities = []
    for entity in entity_response.entities:
        entities.append(
            {
                "name": entity.name,
                "type": language_v1.Entity.Type(entity.type_).name,
                "salience": entity.salience,
                "mentions": [
                    {
                        "text": mention.text.content,
                        "type": language_v1.Reference.Type(mention.type_).name,
                    }
                    for mention in entity.mentions
                ],
            }
        )

    # Classify Text (categories)
    categories_response = client.classify_text(document=document)
    categories = []
    for category in categories_response.categories:
        categories.append(
            {
                "name": category.name,
                "confidence": category.confidence,
            }
        )

    # Determine if content might be sensitive based on sentiment, entities, or categories
    is_sensitive = False
    if (
        sentiment["score"] < -0.2 and sentiment["magnitude"] > 1.0
    ):  # Example threshold for negative sentiment
        is_sensitive = True
    if (
        any(e["type"] in ["PERSON", "LOCATION", "ORGANIZATION"] for e in entities)
        and sentiment["magnitude"] > 1.5
    ):  # Example for personal info with high magnitude
        is_sensitive = True
    if any(
        c["name"].startswith("/Politics") or c["name"].startswith("/Religion")
        for c in categories
    ):  # Example for sensitive categories
        is_sensitive = True

    moderation_results = {
        "original_claim": text_claim,
        "sentiment": sentiment,
        "entities": entities,
        "categories": categories,
        "is_sensitive": is_sensitive,
        "recommendation": "Review manually if is_sensitive is true or if sentiment is strongly negative.",
    }
    return moderation_results


if __name__ == "__main__":
    example_claim = "This user is very angry about the new privacy policy, mentioning specific names and locations."
    moderation_output = moderate_text_claim(example_claim)
    import json

    print(json.dumps(moderation_output, indent=2))

    example_neutral_claim = "The user provided their date of birth as January 1, 1990."
    moderation_output_neutral = moderate_text_claim(example_neutral_claim)
    print("\n--- Neutral Claim Moderation ---")
    print(json.dumps(moderation_output_neutral, indent=2))
