import boto3
import os

class DocumentClient:
    """
    Provides client helper utilities for Structured Document Extraction using AWS Textract.
    """
    def __init__(self, region_name: str = None):
        self.region_name = region_name or os.environ.get("AWS_REGION", "us-east-1")
        self.textract_client = boto3.client(
            'textract',
            region_name=self.region_name,
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
        )

    def get_textract_client(self):
        """
        Returns the configured AWS Textract client.
        """
        return self.textract_client
