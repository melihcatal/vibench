import os
import boto3
from google.cloud import vision
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient

def get_google_vision_client():
    """Returns an authenticated Google Cloud Vision client."""
    # Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    return vision.ImageAnnotatorClient()

def get_aws_textract_client():
    """
    Returns an authenticated AWS Textract client.
    Assumes AWS credentials (e.g., AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    and region (e.g., AWS_REGION) are configured in the environment.
    """
    return boto3.client("textract")

def get_azure_document_intelligence_client():
    """
    Returns an authenticated Azure Document Intelligence client.
    Requires AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY
    environment variables.
    """
    endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")

    if not endpoint or not key:
        raise ValueError(
            "Azure credentials not found in environment variables."
        )

    return DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )
