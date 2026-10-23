import boto3
import os
from typing import Dict, Any

def check_payload_safety(payload: str) -> Dict[str, Any]:
    region = os.getenv('AWS_REGION', 'us-east-1')
    comprehend_client = boto3.client('comprehend', region_name=region)
    response = comprehend_client.detect_toxicity(
        Text=payload,
        LanguageCode='en'
    )
    toxicity_scores = {}
    for label in response['Result']['Labels']:
        toxicity_scores[label['Name']] = label['Score']
    return {
        'is_safe': max(toxicity_scores.values(), default=0.0) < 0.5,
        'scores': toxicity_scores
    }
