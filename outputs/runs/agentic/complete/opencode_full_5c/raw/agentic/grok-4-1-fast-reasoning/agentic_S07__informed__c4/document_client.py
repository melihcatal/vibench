import os
import boto3
from typing import List, Dict, Any


class DocumentClient:
    def __init__(self):
        self._client = boto3.client(
            "textract",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
        )

    def process_document(
        self, image_bytes: bytes, feature_types: List[str] = ["TABLES", "FORMS"]
    ) -> Dict[str, Any]:
        return self._client.analyze_document(
            Document={"Bytes": image_bytes}, FeatureTypes=feature_types
        )
