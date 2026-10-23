from typing import Optional, Dict, Any
import os
from google.cloud import documentai_v1 as documentai
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
import boto3


class DocumentClient:
    """
    Local configuration and client helper utilities for Structured Document Extraction.
    """

    @staticmethod
    def get_google_document_ai_client() -> documentai.DocumentProcessorServiceClient:
        """Initialize Google Document AI client."""
        return documentai.DocumentProcessorServiceClient()

    @staticmethod
    def get_azure_document_intelligence_client() -> DocumentIntelligenceClient:
        """Initialize Azure Document Intelligence client."""
        endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
        key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")
        return DocumentIntelligenceClient(
            endpoint=endpoint, credential=AzureKeyCredential(key)
        )

    @staticmethod
    def get_aws_textract_client() -> boto3.client:
        """Initialize AWS Textract client."""
        return boto3.client(
            "textract",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION", "us-east-1"),
        )

    @staticmethod
    def load_document(file_path: str) -> bytes:
        """Load document content from file."""
        with open(file_path, "rb") as file:
            return file.read()
