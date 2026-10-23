import boto3
from typing import List

class DocumentClient:
    def __init__(self):
        self.client = boto3.client('textract')

    def detect_document_text(self, image_bytes: bytes) -> dict:
        return self.client.detect_document_text(Document={'Bytes': image_bytes})

    def analyze_document(self, image_bytes: bytes, feature_types: List[str]) -> dict:
        return self.client.analyze_document(
            Document={'Bytes': image_bytes},
            FeatureTypes=feature_types
        )
