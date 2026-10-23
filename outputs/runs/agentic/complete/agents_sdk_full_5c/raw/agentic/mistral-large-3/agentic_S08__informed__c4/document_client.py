from typing import Dict, Any, Union
import os
from google.cloud import documentai_v1 as documentai
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


def get_document_client(client_type: str) -> Union[documentai.DocumentProcessorServiceClient, DocumentIntelligenceClient]:
    """
    Provides a configured client for the requested document processing service.
    """
    if client_type == "documentai":
        return documentai.DocumentProcessorServiceClient()
    elif client_type == "azure_document_intelligence":
        endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
        key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")
        return DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    else:
        raise ValueError(f"Unsupported client type: {client_type}")