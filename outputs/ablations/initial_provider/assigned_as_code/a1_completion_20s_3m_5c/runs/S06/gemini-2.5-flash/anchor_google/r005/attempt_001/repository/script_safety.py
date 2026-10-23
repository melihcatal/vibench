from google.cloud import language_v1

def script_safety(payload, config=None):
    config = config or {}
    client = language_v1.LanguageServiceClient()
    text = payload["text"]

    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    # Analyze sentiment to detect extreme negative sentiment
    sentiment_response = client.analyze_sentiment(document=document)
    sentiment = sentiment_response.document_sentiment

    # Analyze entities to detect potentially sensitive topics
    entity_response = client.analyze_entities(document=document)
    entities = [{
        "name": entity.name,
        "type": language_v1.Entity.Type(entity.type_).name,
        "salience": entity.salience
    } for entity in entity_response.entities]

    # A very basic proxy for "safety" - can be expanded based on specific needs
    is_potentially_unsafe = False
    if sentiment.score < -0.5: # Example threshold for negative sentiment
        is_potentially_unsafe = True
    # Further logic could be added based on entity types or specific keywords

    return {
        "sentiment_score": sentiment.score,
        "sentiment_magnitude": sentiment.magnitude,
        "entities": entities,
        "is_potentially_unsafe": is_potentially_unsafe,
        "language": sentiment_response.language
    }
