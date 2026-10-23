from google.cloud import language_v1
from google.cloud.language_v1 import enums

def script_safety(text: str):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type=enums.Document.Type.PLAIN_TEXT)

    # Perform sentiment analysis as a proxy for safety check
    sentiment = client.analyze_sentiment(document=document).document_sentiment

    # Perform entity analysis to identify potential sensitive entities
    entities = client.analyze_entities(document=document).entities

    safety_score = {"score": sentiment.score, "magnitude": sentiment.magnitude}
    detected_entities = [{
        "name": entity.name,
        "type": enums.Entity.Type(entity.type).name,
        "salience": entity.salience
    } for entity in entities]

    # Simple heuristic: if sentiment is very negative or certain entities are present, flag as potentially unsafe
    is_safe = True
    safety_notes = []

    if sentiment.score < -0.5 and sentiment.magnitude > 1.0: # Arbitrary threshold for negative sentiment
        is_safe = False
        safety_notes.append("Strongly negative sentiment detected.")

    # Example of flagging specific entities (can be expanded)
    sensitive_entity_types = [enums.Entity.Type.PERSON, enums.Entity.Type.EVENT, enums.Entity.Type.LOCATION]
    for entity in entities:
        if entity.type in sensitive_entity_types and entity.salience > 0.3: # Arbitrary salience threshold
            # This is a very basic check and would need more sophisticated logic for real safety
            safety_notes.append(f"Potentially sensitive entity '{entity.name}' of type '{enums.Entity.Type(entity.type).name}' detected.")
            is_safe = False

    return {
        "is_safe": is_safe,
        "safety_score": safety_score,
        "detected_entities": detected_entities,
        "safety_notes": safety_notes
    }
