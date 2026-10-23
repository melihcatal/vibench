import os
from typing import Optional, Dict, Any
import boto3
from botocore.config import Config


class DocumentClient:
    """Client helper for Amazon Textract OCR and layout extraction."""

    def __init__(self, region_name: Optional[str] = None):
        """Initialize Textract client with AWS credentials."""
        self.region_name = region_name or os.getenv("AWS_REGION", "us-east-1")

        # AWS credentials from environment variables
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

        if not aws_access_key_id or not aws_secret_access_key:
            raise ValueError(
                "AWS credentials not found. Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables."
            )

        self.client = boto3.client(
            "textract",
            region_name=self.region_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            config=Config(retries={"max_attempts": 3}),
        )

    def detect_document_text(self, document_bytes: bytes) -> Dict[str, Any]:
        """Call Textract DetectDocumentText API."""
        response = self.client.detect_document_text(Document={"Bytes": document_bytes})
        return response

    def analyze_document(
        self, document_bytes: bytes, feature_types: list
    ) -> Dict[str, Any]:
        """Call Textract AnalyzeDocument API for layout and tables."""
        response = self.client.analyze_document(
            Document={"Bytes": document_bytes}, FeatureTypes=feature_types
        )
        return response

    def analyze_expense(self, document_bytes: bytes) -> Dict[str, Any]:
        """Call Textract AnalyzeExpense API for invoice/expense extraction."""
        response = self.client.analyze_expense(Document={"Bytes": document_bytes})
        return response
