from google.cloud import language_v1 as language
from typing import List, Dict


def moderate_transcript(transcript_text: str) -> Dict[str, Any]:
    """Moderate transcript text for harmful content using Google Cloud Natural Language API."""
    client = language.LanguageServiceClient()
    document = language.Document(
        content=transcript_text, type_=language.Document.Type.PLAIN_TEXT
    )

    response = client.analyze_sentiment(request={"document": document})
    sentiment = response.document_sentiment

    response = client.analyze_entity_sentiment(request={"document": document})
    entities = [
        {
            "name": entity.name,
            "type": language.Entity.Type(entity.type_).name,
            "salience": entity.salience,
            "sentiment": entity.sentiment.score,
        }
        for entity in response.entities
    ]

    response = client.moderate_text(request={"document": document})
    moderation = {
        "blocked": response.moderation_categories[0].confidence > 0.7,
        "categories": [
            category.name
            for category in response.moderation_categories
            if category.confidence > 0.5
        ],
    }

    return {
        "sentiment": {"score": sentiment.score, "magnitude": sentiment.magnitude},
        "entities": entities,
        "moderation": moderation,
    }
