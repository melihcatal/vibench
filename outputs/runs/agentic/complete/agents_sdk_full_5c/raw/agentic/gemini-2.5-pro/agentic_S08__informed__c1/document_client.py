import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from mindee import Client as MindeeClient
from google.cloud import documentai
import boto3

def get_document_intelligence_client():
    """Returns an Azure Document Intelligence client."""
    endpoint = os.environ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"]
    key = os.environ["AZURE_DOCUMENT_INTELLIGENCE_KEY"]
    return DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))

def get_mindee_client():
    """Returns a Mindee client."""
    api_key = os.environ["MINDEE_API_KEY"]
    return MindeeClient(api_key=api_key)

def get_google_document_ai_client():
    """Returns a Google Document AI client."""
    # The client uses GOOGLE_APPLICATION_CREDENTIALS environment variable implicitly
    return documentai.DocumentProcessorServiceClient()

def get_textract_client():
    """Returns an AWS Textract client."""
    return boto3.client(
        "textract",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
    )
