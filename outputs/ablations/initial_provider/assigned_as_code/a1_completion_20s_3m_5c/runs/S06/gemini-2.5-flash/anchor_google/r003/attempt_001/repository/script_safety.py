from google.cloud import language_v1

def check_script_safety(text):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Analyze sentiment to check for negative or toxic content
    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment
    
    # Analyze entities to check for specific problematic entities (e.g., hate speech terms)
    # This is a very basic example; real safety checks would be much more complex
    entities = client.analyze_entities(request={'document': document}).entities
    
    safety_score = (sentiment.score + 1) / 2 # Normalize sentiment score to 0-1 range
    
    # A very simplified check for demonstration purposes
    is_safe = safety_score > 0.2 and sentiment.magnitude < 1.0 # Arbitrary thresholds
    
    # You might also look for specific entity types or sentiment of specific entities
    # For a robust solution, consider a dedicated content moderation API or a more sophisticated analysis.

    return {
        "is_safe": is_safe,
        "sentiment_score": sentiment.score,
        "sentiment_magnitude": sentiment.magnitude,
        "entities": [{
            "name": entity.name,
            "type": language_v1.Entity.Type(entity.type_).name,
            "salience": entity.salience
        } for entity in entities]
    }
