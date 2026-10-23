import boto3
from typing import List

def analyze_document(image_path: str, feature_types: List[str]) -> dict:
    client = boto3.client('textract')
    with open(image_path, 'rb') as f:
        image_bytes = f.read()
    response = client.analyze_document(
        Document={'Bytes': image_bytes},
        FeatureTypes=feature_types
    )
    return response
