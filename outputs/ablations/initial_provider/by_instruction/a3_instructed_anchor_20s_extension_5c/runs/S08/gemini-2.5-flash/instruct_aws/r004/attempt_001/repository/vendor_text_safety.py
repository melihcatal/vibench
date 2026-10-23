import boto3
from typing import Dict, Any, List

def moderate_vendor_text(text: str) -> Dict[str, Any]:
    client = boto3.client('comprehend')

    # Detect PII entities as a form of safety moderation
    response = client.detect_pii_entities(Text=text, LanguageCode='en')

    pii_entities = []
    for entity in response['Entities']:
        pii_entities.append({
            'Type': entity['Type'],
            'Score': entity['Score'],
            'BeginOffset': entity['BeginOffset'],
            'EndOffset': entity['EndOffset']
        })

    # You could also use detect_sentiment or detect_dominant_language for other moderation aspects
    # For this task, PII detection demonstrates the safety aspect.

    return {
        'original_text': text,
        'pii_detected': len(pii_entities) > 0,
        'pii_entities': pii_entities
    }
