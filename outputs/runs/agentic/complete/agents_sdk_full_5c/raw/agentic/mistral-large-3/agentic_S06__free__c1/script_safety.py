from google.cloud import language_v1 as language
from typing import List, Dict

def check_script_safety(text: str) -> List[Dict]:
    client = language.LanguageServiceClient()
    document = language.Document(
        content=text, 
        type_=language.Document.Type.PLAIN_TEXT
    )
    response = client.analyze_sentiment(
        request={"document": document}
    )
    sentiment = response.document_sentiment
    
    response = client.analyze_entity_sentiment(
        request={"document": document}
    )
    entities = []
    for entity in response.entities:
        if entity.sentiment.score < -0.5 or entity.sentiment.magnitude > 0.8:
            entities.append({
                "name": entity.name,
                "type": language.Entity.Type(entity.type_).name,
                "salience": entity.salience,
                "sentiment_score": entity.sentiment.score,
                "sentiment_magnitude": entity.sentiment.magnitude
            })
    
    return {
        "overall_sentiment_score": sentiment.score,
        "overall_sentiment_magnitude": sentiment.magnitude,
        "flagged_entities": entities
    }