from google.cloud import language_v1
from document_client import get_google_cloud_language_config # For consistency, though not strictly needed for default credentials

def moderate_vendor_notes(text_content: str) -> dict:
    # Google Cloud client libraries typically handle authentication automatically
    # based on environment variables (e.g., GOOGLE_APPLICATION_CREDENTIALS)
    client = language_v1.LanguageServiceClient()
    
    document = language_v1.Document(content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Analyze sentiment to detect potentially negative or unsafe language
    sentiment_response = client.analyze_sentiment(document=document, encoding_type=language_v1.EncodingType.UTF8)
    sentiment_score = sentiment_response.document_sentiment.score
    sentiment_magnitude = sentiment_response.document_sentiment.magnitude

    # Analyze entities to see if any problematic entities are mentioned
    entity_response = client.analyze_entities(document=document, encoding_type=language_v1.EncodingType.UTF8)
    entities = [{'name': entity.name, 'type': language_v1.Entity.Type(entity.type_).name, 'salience': entity.salience} for entity in entity_response.entities]

    # Analyze syntax for more advanced linguistic checks if needed (omitted for brevity)

    # Basic safety check based on sentiment
    is_safe = True
    safety_notes = []

    if sentiment_score < -0.5 and sentiment_magnitude > 1.0:
        is_safe = False
        safety_notes.append("Strongly negative sentiment detected, may contain unsafe language.")
    elif sentiment_score < -0.2:
        safety_notes.append("Negative sentiment detected, review for potential issues.")
    
    # Further checks based on entities could be added here
    # e.g., if any entity type or specific entity name is on a blacklist

    return {
        "text_content": text_content,
        "is_safe": is_safe,
        "sentiment_score": sentiment_score,
        "sentiment_magnitude": sentiment_magnitude,
        "entities": entities,
        "safety_notes": safety_notes
    }
