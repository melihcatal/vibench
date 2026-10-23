import os
from typing import Optional, Dict, Any
from google.cloud import documentai
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
import boto3
from mindee import Client


class DocumentClient:
    """Provide local configuration and client helper utilities for OCR and Layout Extraction."""

    @staticmethod
    def get_documentai_client() -> documentai.DocumentProcessorServiceClient:
        """Get Google Document AI client."""
        return documentai.DocumentProcessorServiceClient()

    @staticmethod
    def get_azure_document_client() -> DocumentIntelligenceClient:
        """Get Azure Document Intelligence client."""
        endpoint = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
        key = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY")

        if not endpoint or not key:
            raise ValueError("Azure Document Intelligence credentials not configured")

        credential = AzureKeyCredential(key)
        return DocumentIntelligenceClient(endpoint=endpoint, credential=credential)

    @staticmethod
    def get_textract_client():
        """Get Amazon Textract client."""
        return boto3.client(
            "textract",
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
            region_name=os.environ.get("AWS_REGION", "us-east-1"),
        )

    @staticmethod
    def get_mindee_client() -> Client:
        """Get Mindee client."""
        api_key = os.environ.get("MINDEE_API_KEY")
        if not api_key:
            raise ValueError("MINDEE_API_KEY environment variable is required")
        return Client(api_key=api_key)

    @staticmethod
    def load_config() -> Dict[str, Any]:
        """Load configuration from environment variables."""
        config = {
            "google": {
                "project_id": os.environ.get("GOOGLE_CLOUD_PROJECT"),
                "location": os.environ.get("DOCUMENTAI_LOCATION", "us"),
                "processor_id": os.environ.get("DOCUMENTAI_PROCESSOR_ID"),
            },
            "azure": {
                "endpoint": os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"),
                "key": os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY"),
            },
            "aws": {
                "access_key_id": os.environ.get("AWS_ACCESS_KEY_ID"),
                "secret_access_key": os.environ.get("AWS_SECRET_ACCESS_KEY"),
                "region": os.environ.get("AWS_REGION", "us-east-1"),
            },
            "mindee": {"api_key": os.environ.get("MINDEE_API_KEY")},
        }
        return config

    @staticmethod
    def validate_config(config: Dict[str, Any]) -> bool:
        """Validate that required configuration is present."""
        required_providers = []

        if config["google"]["project_id"] and config["google"]["processor_id"]:
            required_providers.append("google")

        if config["azure"]["endpoint"] and config["azure"]["key"]:
            required_providers.append("azure")

        if config["aws"]["access_key_id"] and config["aws"]["secret_access_key"]:
            required_providers.append("aws")

        if config["mindee"]["api_key"]:
            required_providers.append("mindee")

        return len(required_providers) > 0
