import os
from google.cloud import language_v1
from google.cloud.language_v1 import enums

def profile_moderation(profile_text: str) -> dict:
    # Google Cloud Natural Language API client initialization
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    client = language_v1.LanguageServiceClient()

    document = language_v1.types.Document(
        content=profile_text,
        type=enums.Document.Type.PLAIN_TEXT
    )

    # Perform sentiment analysis
    sentiment = client.analyze_sentiment(document=document).document_sentiment

    # Perform entity analysis
    entities = client.analyze_entities(document=document, encoding_type=enums.EncodingType.UTF8).entities

    # Simple moderation logic based on sentiment and detected entities
    # This is a basic example; real moderation would be more sophisticated.
    is_flagged = False
    flag_reasons = []

    if sentiment.score < -0.5: # Very negative sentiment
        is_flagged = True
        flag_reasons.append("Strongly negative sentiment detected.")

    # Check for specific entity types that might be sensitive or require review
    sensitive_entity_types = {
        enums.Entity.Type.PERSON, 
        enums.Entity.Type.LOCATION, 
        enums.Entity.Type.ORGANIZATION, 
        enums.Entity.Type.EVENT,
        enums.Entity.Type.WORK_OF_ART,
        enums.Entity.Type.CONSUMER_GOOD
    }
    
    for entity in entities:
        if entity.type in sensitive_entity_types:
            # This is a very simplistic check. In a real scenario, you'd have a list of
            # problematic keywords or more advanced NLP rules.
            if len(entity.name.split()) > 1: # Flag multi-word entities as potentially sensitive for review
                 is_flagged = True
                 flag_reasons.append(f"Potentially sensitive entity detected: {entity.name} (Type: {enums.Entity.Type(entity.type).name}).")

    return {
        "original_text": profile_text,
        "sentiment_score": sentiment.score,
        "sentiment_magnitude": sentiment.magnitude,
        "entities": [{
            "name": entity.name,
            "type": enums.Entity.Type(entity.type).name,
            "salience": entity.salience
        } for entity in entities],
        "is_flagged_for_review": is_flagged,
        "flag_reasons": flag_reasons
    }
