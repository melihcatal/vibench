import boto3
from typing import Optional, List
from pathlib import Path

def get_textract_client(region: Optional[str] = None) -> boto3.client:
    return boto3.client('textract', region_name=region or 'us-east-1')

def detect_document_text(image_path: str) -> dict:
    image_bytes = Path(image_path).read_bytes()
    client = get_textract_client()
    return client.detect_document_text(Document={'Bytes': image_bytes})

def analyze_document(image_path: str, feature_types: List[str]) -> dict:
    image_bytes = Path(image_path).read_bytes()
    client = get_textract_client()
    return client.analyze_document(
        Document={'Bytes': image_bytes},
        FeatureTypes=feature_types
    )
