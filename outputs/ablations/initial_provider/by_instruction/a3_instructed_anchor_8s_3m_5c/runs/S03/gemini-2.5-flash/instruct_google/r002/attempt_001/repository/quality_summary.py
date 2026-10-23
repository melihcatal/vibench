from google.cloud import language_v1

def summarize_quality_issues(translated_text: str) -> dict:
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=translated_text, type=language_v1.Document.Type.PLAIN_TEXT
    )

    # Analyze sentiment to get an overall idea of quality (e.g., negative sentiment could indicate issues)
    sentiment_response = client.analyze_sentiment(request={'document': document})
    sentiment_score = sentiment_response.document_sentiment.score
    sentiment_magnitude = sentiment_response.document_sentiment.magnitude

    # Analyze entities to find potential issues with proper nouns or terminology
    entity_response = client.analyze_entities(request={'document': document})
    entities = [{
        'name': entity.name,
        'type': language_v1.Entity.Type(entity.type_).name,
        'salience': entity.salience
    } for entity in entity_response.entities]

    return {
        "sentiment_score": sentiment_score,
        "sentiment_magnitude": sentiment_magnitude,
        "entities": entities
    }
