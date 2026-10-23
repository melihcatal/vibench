"""
Local configuration and client helper utilities for Structured Document Extraction.
"""
import os
import boto3
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from google.cloud import documentai
from mindee import Client as MindeeClient

def get_azure_document_intelligence_client():
    """Returns an Azure Document Intelligence client."""
    endpoint = os.environ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"]
    key = os.environ["AZURE_DOCUMENT_INTELLIGENCE_KEY"]
    return DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))

def get_aws_textract_client():
    """Returns an AWS Textract client."""
    return boto3.client(
        "textract",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
    )

def get_google_document_ai_client():
    """Returns a Google Document AI client."""
    # Assumes GOOGLE_APPLICATION_CREDENTIALS is set
    opts = {"api_endpoint": f"us-documentai.googleapis.com"}
    return documentai.DocumentProcessorServiceClient(client_options=opts)


def get_mindee_client():
    """Returns a Mindee client."""
    # Assumes MINDEE_API_KEY is set in the environment
    return MindeeClient()
