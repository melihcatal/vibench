import os
from google.cloud import language_v1
from typing import List, Dict

def moderate_transcript_text(text: str, project_id: str = None) -> Dict:
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Classify text content for moderation
    response = client.classify_text(request={'document': document})
    
    # Analyze sentiment for additional moderation insights
    sentiment_response = client.analyze_sentiment(request={'document': document})

    # Analyze entities for potential sensitive information
    entity_response = client.analyze_entities(request={'document': document})

    categories = [{'name': category.name, 'confidence': category.confidence} for category in response.categories]
    sentiment = {
        'score': sentiment_response.document_sentiment.score,
        'magnitude': sentiment_response.document_sentiment.magnitude
    }
    entities = [{'name': entity.name, 'type': language_v1.Entity.Type(entity.type_).name, 'salience': entity.salience} for entity in entity_response.entities]

    return {
        "categories": categories,
        "sentiment": sentiment,
        "entities": entities,
    }
