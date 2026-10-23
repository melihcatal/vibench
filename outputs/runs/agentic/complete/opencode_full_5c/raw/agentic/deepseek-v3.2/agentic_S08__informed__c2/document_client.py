import os
from typing import Dict, Any, Optional
import boto3
from botocore.exceptions import ClientError


class DocumentClient:
    """Client helper for Amazon Textract AnalyzeExpense service."""

    def __init__(self, region_name: str = None):
        """Initialize Textract client."""
        self.region_name = region_name or os.getenv("AWS_DEFAULT_REGION", "us-east-1")
        self.client = boto3.client(
            "textract",
            region_name=self.region_name,
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )

    def analyze_expense(self, document_bytes: bytes) -> Dict[str, Any]:
        """Analyze expense document using Amazon Textract AnalyzeExpense."""
        try:
            response = self.client.analyze_expense(Document={"Bytes": document_bytes})
            return response
        except ClientError as e:
            raise Exception(f"Textract AnalyzeExpense error: {e}")

    def analyze_document(
        self, document_bytes: bytes, feature_types: list = None
    ) -> Dict[str, Any]:
        """Analyze document using Textract AnalyzeDocument."""
        if feature_types is None:
            feature_types = ["FORMS", "TABLES"]

        try:
            response = self.client.analyze_document(
                Document={"Bytes": document_bytes}, FeatureTypes=feature_types
            )
            return response
        except ClientError as e:
            raise Exception(f"Textract AnalyzeDocument error: {e}")

    @staticmethod
    def load_config() -> Dict[str, Any]:
        """Load configuration from environment variables."""
        return {
            "aws_region": os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
            "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID"),
            "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
            "textract_service": "Amazon Textract AnalyzeExpense",
        }
