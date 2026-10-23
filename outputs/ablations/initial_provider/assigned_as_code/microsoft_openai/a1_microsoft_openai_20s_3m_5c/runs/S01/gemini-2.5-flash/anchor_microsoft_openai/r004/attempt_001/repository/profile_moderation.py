from google.cloud import language_v1
import os
from identity_models import ModerationRequest

def profile_moderation(payload: ModerationRequest) -> dict:
    # Google Cloud Natural Language API client initialization
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or authenticate otherwise.

    client = language_v1.LanguageServiceClient()

    text_content = payload.text

    # Prepare the document for the API request
    document = language_v1.Document(
        content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    # Perform sentiment analysis
    sentiment_response = client.analyze_sentiment(document=document)
    sentiment = sentiment_response.document_sentiment

    # Perform entity analysis (can help identify sensitive topics)
    entity_response = client.analyze_entities(document=document)
    entities = [{'name': entity.name, 'type': language_v1.Entity.Type(entity.type_).name, 'salience': entity.salience} for entity in entity_response.entities]

    # Basic moderation logic: Flag if sentiment is very negative
    is_flagged = False
    if sentiment.score < -0.5 and sentiment.magnitude > 1.0:
        is_flagged = True

    return {
        "text": text_content,
        "sentiment_score": sentiment.score,
        "sentiment_magnitude": sentiment.magnitude,
        "entities": entities,
        "is_flagged_for_moderation": is_flagged,
        "moderation_notes": "Flagged if sentiment is very negative (score < -0.5 and magnitude > 1.0)"
    }
