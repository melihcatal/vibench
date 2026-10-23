import boto3
from typing import Dict, Any

def get_aws_comprehend_client():
    return boto3.client('comprehend')

def parse_aws_comprehend_moderation_response(response: Dict[str, Any]) -> Dict[str, float]:
    categories = {}
    for result in response.get('ModerationLabels', []):
        name = result.get('Name')
        score = result.get('Score')
        if name and score:
            categories[name] = score
    return categories
