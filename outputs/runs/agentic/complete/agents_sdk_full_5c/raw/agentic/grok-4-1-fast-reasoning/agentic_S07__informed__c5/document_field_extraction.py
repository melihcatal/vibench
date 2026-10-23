import boto3
import os
from typing import Dict, List

def document_field_extraction(text: str) -> Dict[str, Any]:
    """
    Extract structured fields from OCR-normalized document text using Amazon Comprehend.
    """
    client = boto3.client('comprehend', region_name=os.getenv('AWS_REGION', 'us-east-1'))
    
    # Detect entities
    entities_response = client.detect_entities(
        Text=text,
        LanguageCode='en'
    )
    
    fields: Dict[str, Any] = {}
    for entity in entities_response['Entities']:
        entity_type = entity['Type']
        if entity_type == 'ORGANIZATION':
            fields.setdefault('vendor', []).append(entity['Text'])
        elif entity_type == 'DATE':
            fields.setdefault('date', []).append(entity['Text'])
        elif entity_type == 'MONEY':
            fields.setdefault('amount', []).append(entity['Text'])
        elif entity_type == 'COMMERCIAL_ITEM':
            fields.setdefault('items', []).append(entity['Text'])
    
    # Detect PII for additional fields
    pii_response = client.detect_pii_entities(Text=text, LanguageCode='en')
    for entity in pii_response['Entities']:
        if entity['Type'] == 'NAME':
            fields['customer_name'] = entity['Text']
    
    return fields
