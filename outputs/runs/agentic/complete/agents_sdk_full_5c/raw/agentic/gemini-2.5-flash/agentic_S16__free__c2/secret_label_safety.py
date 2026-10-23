import os
from google.cloud import language_v1
from typing import Dict, Any

def check_secret_label_safety(text_to_analyze: str) -> Dict[str, Any]:
    """
    Checks secret labels and notes for unsafe text using Google Cloud Natural Language API.
    """
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(content=text_to_analyze, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Detect sentiment
    sentiment_response = client.analyze_sentiment(request={'document': document})
    sentiment = sentiment_response.document_sentiment

    # Detect entities (useful for identifying sensitive info like names, locations)
    entities_response = client.analyze_entities(request={'document': document, 'encoding_type': language_v1.EncodingType.UTF8})
    entities = [{'name': entity.name, 'type': entity.type_.name, 'salience': entity.salience} for entity in entities_response.entities]

    # You can define custom rules based on sentiment score or detected entities
    is_unsafe = False
    safety_notes = []

    if sentiment.score < -0.5: # Example threshold for negative sentiment
        is_unsafe = True
        safety_notes.append(f"Very negative sentiment detected (score: {sentiment.score}).")
    
    # Example: Look for specific entity types that might indicate sensitive data
    sensitive_entity_types = {'PERSON', 'LOCATION', 'PHONE_NUMBER', 'CREDIT_CARD_NUMBER'}
    for entity in entities:
        if entity['type'] in sensitive_entity_types:
            is_unsafe = True
            safety_notes.append(f"Potentially sensitive entity detected: {entity['type']} - {entity['name']}")

    return {
        "text_analyzed": text_to_analyze,
        "sentiment_score": sentiment.score,
        "sentiment_magnitude": sentiment.magnitude,
        "entities": entities,
        "is_unsafe": is_unsafe,
        "safety_notes": safety_notes
    }

if __name__ == "__main__":
    # Example usage:
    # Set GOOGLE_APPLICATION_CREDENTIALS environment variable or use gcloud auth
    # label_text = "This secret contains highly confidential production database credentials. Do not share."
    # safety_report = check_secret_label_safety(label_text)
    # print(f"Safety Report: {safety_report}")

    # label_text_safe = "This is a test label for a non-sensitive secret."
    # safety_report_safe = check_secret_label_safety(label_text_safe)
    # print(f"Safety Report (Safe): {safety_report_safe}")
    pass
