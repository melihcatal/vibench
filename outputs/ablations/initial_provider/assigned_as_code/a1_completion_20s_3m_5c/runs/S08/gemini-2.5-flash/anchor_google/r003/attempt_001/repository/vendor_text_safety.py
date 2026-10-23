from google.cloud import language_v1

def moderate_vendor_text_safety(text_content, config=None):
    config = config or {}
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Perform sentiment analysis
    sentiment_response = client.analyze_sentiment(document=document)
    sentiment = sentiment_response.document_sentiment

    # Perform entity analysis to identify potential issues (e.g., sensitive entities)
    entity_response = client.analyze_entities(document=document, encoding_type=language_v1.EncodingType.UTF8)
    entities = entity_response.entities

    safety_score = {
        "overall_sentiment": sentiment.score,
        "overall_magnitude": sentiment.magnitude,
        "potentially_sensitive_entities": []
    }

    # Example: identify entities with certain categories or salience that might be sensitive
    for entity in entities:
        # This is a simplified example; a real-world scenario would involve
        # more sophisticated rules for identifying sensitive content based on entity types,
        # sentiment towards entities, or custom entity recognition models.
        if entity.salience > 0.1 and (entity.type_ == language_v1.Entity.Type.PERSON or entity.type_ == language_v1.Entity.Type.ORGANIZATION):
            safety_score["potentially_sensitive_entities"].append({
                "name": entity.name,
                "type": language_v1.Entity.Type(entity.type_).name,
                "salience": entity.salience
            })
    
    # Determine overall safety status based on scores and identified entities
    is_safe = True
    if sentiment.score < -0.5 and sentiment.magnitude > 1.0: # Very negative sentiment
        is_safe = False
    if len(safety_score["potentially_sensitive_entities"]) > 0:
        is_safe = False # Presence of sensitive entities might indicate unsafe content

    return {"is_safe": is_safe, "analysis_results": safety_score}