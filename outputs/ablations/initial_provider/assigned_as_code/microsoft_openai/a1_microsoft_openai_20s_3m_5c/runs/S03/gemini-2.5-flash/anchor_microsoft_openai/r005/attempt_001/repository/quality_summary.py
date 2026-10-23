from google.cloud import language_v2
import os

def quality_summary(payload):
    client = language_v2.LanguageServiceClient()
    text_content = payload['text']

    document = language_v2.Document(content=text_content, type_=language_v2.Document.Type.PLAIN_TEXT)
    
    # Perform sentiment analysis
    sentiment_response = client.analyze_sentiment(document=document)
    sentiment = sentiment_response.document_sentiment

    # Perform entity analysis
    entity_response = client.analyze_entities(document=document)
    entities = entity_response.entities

    # Summarize findings
    summary = {
        "sentiment_score": sentiment.score,
        "sentiment_magnitude": sentiment.magnitude,
        "entities": [{
            "name": entity.name,
            "type": language_v2.Entity.Type(entity.type_).name,
            "salience": entity.salience
        } for entity in entities]
    }
    
    return summary
