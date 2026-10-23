import os
from typing import Optional, Dict, Any
import boto3
from botocore.exceptions import ClientError


class DocumentClient:
    """Client helper for Amazon Textract OCR and layout extraction."""

    def __init__(self, region_name: Optional[str] = None):
        """Initialize Textract client.

        Args:
            region_name: AWS region name. Defaults to AWS_DEFAULT_REGION env var.
        """
        self.region_name = region_name or os.getenv("AWS_DEFAULT_REGION", "us-east-1")
        self.client = boto3.client(
            "textract",
            region_name=self.region_name,
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )

    def analyze_document(
        self, document_bytes: bytes, feature_types: list
    ) -> Dict[str, Any]:
        """Analyze document with Textract.

        Args:
            document_bytes: Document image bytes
            feature_types: List of feature types to extract

        Returns:
            Textract response
        """
        try:
            response = self.client.analyze_document(
                Document={"Bytes": document_bytes}, FeatureTypes=feature_types
            )
            return response
        except ClientError as e:
            raise Exception(f"Textract API error: {e}")

    def detect_document_text(self, document_bytes: bytes) -> Dict[str, Any]:
        """Detect text in document.

        Args:
            document_bytes: Document image bytes

        Returns:
            Textract response
        """
        try:
            response = self.client.detect_document_text(
                Document={"Bytes": document_bytes}
            )
            return response
        except ClientError as e:
            raise Exception(f"Textract API error: {e}")
