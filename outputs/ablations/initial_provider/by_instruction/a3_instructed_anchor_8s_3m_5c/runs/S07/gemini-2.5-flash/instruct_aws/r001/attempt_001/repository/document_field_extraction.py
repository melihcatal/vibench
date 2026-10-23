import boto3
from document_client import get_comprehend_client
from typing import List, Dict, Any

def extract_fields_from_text(text: str, entity_recognizer_arn: str) -> List[Dict[str, Any]]:
    """
    Extracts structured fields (custom entities) from OCR-normalized document text using AWS Comprehend.
    Requires a pre-trained custom entity recognizer specified by its ARN.
    """
    comprehend_client = get_comprehend_client()
    response = comprehend_client.detect_custom_entities(
        Text=text,
        EndpointArn=entity_recognizer_arn
    )

    extracted_fields: List[Dict[str, Any]] = []
    for entity in response.get('Entities', []):
        extracted_fields.append({
            "text": entity['Text'],
            "type": entity['Type'],
            "score": entity['Score'],
            "begin_offset": entity['BeginOffset'],
            "end_offset": entity['EndOffset']
        })
    return extracted_fields
