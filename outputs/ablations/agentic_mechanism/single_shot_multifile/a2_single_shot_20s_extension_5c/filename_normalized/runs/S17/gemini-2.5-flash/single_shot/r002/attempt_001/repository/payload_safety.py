import os
from typing import List
import boto3
from security_client import get_comprehend_client
from security_models import PIIEntity

def check_payload_for_pii(text_payload: str, language_code: str = 'en') -> List[PIIEntity]:
    """Checks a text payload for Personally Identifiable Information (PII) using AWS Comprehend."""
    comprehend_client = get_comprehend_client()

    detected_pii: List[PIIEntity] = []
    try:
        # AWS Comprehend offers 'DetectPiiEntities' for PII detection.
        # Other options include 'DetectSentiment', 'DetectSyntax', etc., for general unsafe content.
        response = comprehend_client.detect_pii_entities(
            Text=text_payload,
            LanguageCode=language_code  # e.g., 'en', 'es', 'fr', 'de', 'it', 'pt'
        )

        for entity in response.get('Entities', []):
            pii_entity = PIIEntity(
                text=text_payload[entity['BeginOffset']:entity['EndOffset']],
                type=entity['Type'],
                score=entity['Score'],
                begin_offset=entity['BeginOffset'],
                end_offset=entity['EndOffset']
            )
            detected_pii.append(pii_entity)

    except Exception as e:
        raise RuntimeError(f"Failed to detect PII with AWS Comprehend: {e}")

    return detected_pii