import os
from typing import Optional, Dict, Any
import boto3
from botocore.exceptions import ClientError


class DocumentClient:
    """Client helper for Amazon Textract AnalyzeExpense service."""

    def __init__(self, region_name: Optional[str] = None):
        self.region_name = region_name or os.getenv("AWS_REGION", "us-east-1")
        self.client = self._create_client()

    def _create_client(self):
        """Create and return Textract client."""
        return boto3.client(
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

    def get_config(self) -> Dict[str, Any]:
        """Get client configuration."""
        return {
            "service": "Amazon Textract AnalyzeExpense",
            "region": self.region_name,
            "auth_vars": ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"],
        }
