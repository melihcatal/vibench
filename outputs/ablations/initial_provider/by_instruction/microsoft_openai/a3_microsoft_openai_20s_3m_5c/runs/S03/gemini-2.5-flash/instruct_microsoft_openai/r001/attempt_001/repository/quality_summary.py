from google.cloud import language_v1
import os

def summarize_translation_quality(text: str) -> dict:
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Perform sentiment analysis
    sentiment_response = client.analyze_sentiment(document=document)
    sentiment = sentiment_response.document_sentiment

    # Perform entity analysis
    entity_response = client.analyze_entities(document=document, encoding_type=language_v1.EncodingType.UTF8)
    entities = [{'name': entity.name, 'type': language_v1.Entity.Type(entity.type_).name, 'salience': entity.salience} for entity in entity_response.entities]

    return {
        "sentiment_score": sentiment.score,
        "sentiment_magnitude": sentiment.magnitude,
        "entities": entities
    }
