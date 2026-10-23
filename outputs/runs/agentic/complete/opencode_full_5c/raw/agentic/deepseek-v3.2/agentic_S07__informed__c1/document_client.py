import os
import boto3
from typing import Optional, Dict, Any


class DocumentClient:
    def __init__(self, region_name: Optional[str] = None):
        self.region_name = region_name or os.getenv("AWS_REGION", "us-east-1")
        self.textract_client = None
        self.translate_client = None
        self.comprehend_client = None
        self.bedrock_client = None

    def get_textract_client(self):
        if self.textract_client is None:
            self.textract_client = boto3.client(
                "textract",
                region_name=self.region_name,
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            )
        return self.textract_client

    def get_translate_client(self):
        if self.translate_client is None:
            self.translate_client = boto3.client(
                "translate",
                region_name=self.region_name,
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            )
        return self.translate_client

    def get_comprehend_client(self):
        if self.comprehend_client is None:
            self.comprehend_client = boto3.client(
                "comprehend",
                region_name=self.region_name,
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            )
        return self.comprehend_client

    def get_bedrock_client(self):
        if self.bedrock_client is None:
            self.bedrock_client = boto3.client(
                "bedrock-runtime",
                region_name=self.region_name,
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            )
        return self.bedrock_client

    def read_image_bytes(self, image_path: str) -> bytes:
        with open(image_path, "rb") as f:
            return f.read()

    def prepare_textract_request(self, image_bytes: bytes) -> Dict[str, Any]:
        return {"Document": {"Bytes": image_bytes}}

    def get_textract_features(self, feature_type: str) -> list:
        feature_map = {
            "text": ["TABLES", "FORMS"],
            "layout": ["LAYOUT"],
            "tables": ["TABLES"],
            "key_values": ["FORMS"],
        }
        return feature_map.get(feature_type, ["TABLES", "FORMS"])
