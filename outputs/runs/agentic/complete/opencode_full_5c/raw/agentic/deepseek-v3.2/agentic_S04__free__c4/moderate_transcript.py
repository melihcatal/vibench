import os
from google.cloud import language_v1
from google.cloud.language_v1 import enums


def moderate_transcript(transcript_text):
    """Moderate transcript text before publishing using Google Cloud Natural Language API."""
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable must be set"
        )

    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=transcript_text,
        type_=enums.Document.Type.PLAIN_TEXT,
    )

    # Analyze sentiment
    sentiment_response = client.analyze_sentiment(document=document)

    # Analyze entities
    entities_response = client.analyze_entities(document=document)

    # Moderate content (check for sensitive content)
    moderation_result = {
        "sentiment_score": sentiment_response.document_sentiment.score,
        "sentiment_magnitude": sentiment_response.document_sentiment.magnitude,
        "entity_count": len(entities_response.entities),
        "contains_sensitive_content": False,
        "flagged_entities": [],
    }

    # Check for potentially sensitive entities
    sensitive_types = ["PERSON", "LOCATION", "ORGANIZATION", "PHONE_NUMBER", "ADDRESS"]
    for entity in entities_response.entities:
        if entity.type_.name in sensitive_types:
            moderation_result["flagged_entities"].append(
                {
                    "name": entity.name,
                    "type": entity.type_.name,
                    "salience": entity.salience,
                }
            )

    if moderation_result["flagged_entities"]:
        moderation_result["contains_sensitive_content"] = True

    return moderation_result
