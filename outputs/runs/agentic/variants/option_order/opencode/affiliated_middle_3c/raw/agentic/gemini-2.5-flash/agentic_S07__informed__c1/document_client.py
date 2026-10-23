import os
from google.cloud import documentai_v1beta3 as documentai
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
import boto3
from mindee import Client, product


class DocumentAIClient:
    def __init__(self):
        # GOOGLE_APPLICATION_CREDENTIALS should be set in environment
        self.client = documentai.DocumentProcessorServiceClient()


class AzureDocumentIntelligenceClient:
    def __init__(self):
        endpoint = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
        key = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY")
        if not endpoint or not key:
            raise ValueError(
                "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY must be set in environment."
            )
        self.client = DocumentIntelligenceClient(
            endpoint=endpoint, credential=AzureKeyCredential(key)
        )


class AmazonTextractClient:
    def __init__(self):
        # AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY should be set in environment
        self.client = boto3.client("textract")


class MindeeClient:
    def __init__(self):
        api_key = os.environ.get("MINDEE_API_KEY")
        if not api_key:
            raise ValueError("MINDEE_API_KEY must be set in environment.")
        self.client = Client(api_key=api_key)
