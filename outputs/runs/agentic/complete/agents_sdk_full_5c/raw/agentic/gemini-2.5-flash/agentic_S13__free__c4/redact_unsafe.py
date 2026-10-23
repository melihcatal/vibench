import boto3
import os

def redact_unsafe_text(text: str, language_code: str = 'en') -> str:
    comprehend_client = boto3.client(
        'comprehend',
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
    )

    # Detect PII entities
    detect_response = comprehend_client.detect_pii_entities(
        Text=text,
        LanguageCode=language_code
    )
    
    # Create PII entities object for redaction
    pii_entities = []
    for entity in detect_response['Entities']:
        pii_entities.append({
            'Type': entity['Type'],
            'BeginOffset': entity['BeginOffset'],
            'EndOffset': entity['EndOffset']
        })

    if not pii_entities:
        return text # No PII to redact

    # Redact PII entities
    redact_response = comprehend_client.redact_pii_entities(
        Text=text,
        LanguageCode=language_code,
        RedactionConfig={
            'PiiEntityType': 'ALL', # Redact all detected PII types
            'MaskMode': 'REPLACE_WITH_CHARACTER',
            'MaskCharacter': '*'
        }
    )
    
    return redact_response['RedactedText']
