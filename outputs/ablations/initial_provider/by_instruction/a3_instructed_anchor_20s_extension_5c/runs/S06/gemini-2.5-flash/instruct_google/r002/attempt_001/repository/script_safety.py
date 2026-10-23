from google.cloud import language_v1

def analyze_sentiment_and_entities(text_content: str):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT)

    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment
    entities = client.analyze_entities(request={'document': document}).entities

    # A simplistic safety check: flag if sentiment is very negative or certain entity types are present.
    # In a real scenario, this would involve more sophisticated rules and potentially a specialized API like Perspective API.
    is_unsafe = False
    safety_notes = []

    if sentiment.score < -0.5:
        is_unsafe = True
        safety_notes.append(f"Very negative sentiment detected (score: {sentiment.score}).")

    # Example: Check for certain entity types that might indicate sensitive content
    sensitive_entity_types = {
        language_v1.Entity.Type.PERSON,
        language_v1.Entity.Type.LOCATION,
        language_v1.Entity.Type.EVENT,
        language_v1.Entity.Type.CONSUMER_GOOD,
        language_v1.Entity.Type.OTHER # Catch-all for potentially unclassified sensitive info
    }

    for entity in entities:
        if entity.type in sensitive_entity_types:
            is_unsafe = True
            safety_notes.append(f"Potentially sensitive entity type '{language_v1.Entity.Type(entity.type).name}' found: '{entity.name}'.")

    return {"is_unsafe": is_unsafe, "safety_notes": safety_notes, "sentiment": sentiment, "entities": entities}
