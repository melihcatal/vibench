import os
from typing import Optional
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


def get_document_intelligence_client() -> DocumentIntelligenceClient:
    """Initialize and return Azure Document Intelligence client."""
    endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")
    
    if not endpoint or not key:
        raise ValueError(
            "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY "
            "must be set in environment variables."
        )
    
    return DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))