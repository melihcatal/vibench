import boto3
import os
from typing import List, Dict, Any

def embed_moderation_rationales_aws(rationales: List[str]) -> List[Dict[str, Any]]:
    """
    Extracts entities from moderation rationales for case retrieval using AWS Comprehend.
    This serves as a proxy for 'embedding' by providing structured data for retrieval.
    """
    comprehend = boto3.client(
        'comprehend',
        region_name=os.environ.get('AWS_REGION', 'us-east-1'),
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )

    all_extracted_entities = []
    for rationale_text in rationales:
        response = comprehend.detect_entities(Text=rationale_text, LanguageCode='en')
        
        entities_for_rationale = []
        for entity in response['Entities']:
            entities_for_rationale.append({
                'text': entity['Text'],
                'type': entity['Type'],
                'score': entity['Score']
            })
        all_extracted_entities.append({
            'original_rationale': rationale_text,
            'extracted_entities': entities_for_rationale,
            'provider': 'AWS Comprehend'
        })
    return all_extracted_entities
