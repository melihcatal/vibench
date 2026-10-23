import os
from typing import Dict, Any, Optional
import boto3
from botocore.exceptions import ClientError


class DocumentClient:
    """
    Client helper for AWS Textract AnalyzeExpense.
    """

    def __init__(self):
        self.client = boto3.client(
            "textract",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION", "us-east-1"),
        )

    def analyze_expense(self, document_bytes: bytes) -> Dict[str, Any]:
        """
        Calls AWS Textract AnalyzeExpense API.
        """
        try:
            response = self.client.analyze_expense(Document={"Bytes": document_bytes})
            return response
        except ClientError as e:
            raise Exception(f"AWS Textract AnalyzeExpense failed: {e}")

    def analyze_document(
        self, document_bytes: bytes, feature_types: list
    ) -> Dict[str, Any]:
        """
        Calls AWS Textract AnalyzeDocument API for generic document analysis.
        """
        try:
            response = self.client.analyze_document(
                Document={"Bytes": document_bytes}, FeatureTypes=feature_types
            )
            return response
        except ClientError as e:
            raise Exception(f"AWS Textract AnalyzeDocument failed: {e}")
