import os
import boto3
from typing import Dict, Any

def document_field_extraction(text: str) -> Dict[str, Any]:
    access_key = os.getenv('AWS_ACCESS_KEY_ID')
    secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    region = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
    if not access_key or not secret_key:
        raise ValueError("AWS credentials must be set.")
    comprehend = boto3.client(
        'comprehend',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region
    )
    response = comprehend.detect_entities(Text=text, LanguageCode='en')
    return {'entities': response['Entities']}