import os
from google.cloud import documentai_v1beta3 as documentai
import boto3


def get_document_ai_client():
    """Initializes and returns a Google Document AI client."""
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    return documentai.DocumentProcessorServiceClient()


def get_textract_client():
    """Initializes and returns an Amazon Textract client."""
    # AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables should be set
    return boto3.client("textract", region_name="us-east-1")  # Example region
