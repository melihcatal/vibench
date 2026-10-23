import os
from typing import Optional, Union
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from google.cloud import documentai_v1 as documentai


def get_document_client(
    provider: str, 
    endpoint: Optional[str] = None,
    key: Optional[str] = None,
    processor_id: Optional[str] = None,
    location: Optional[str] = None,
    project_id: Optional[str] = None,
) -> Union[DocumentIntelligenceClient, documentai.DocumentProcessorServiceClient]:
    """
    Provides a configured client for structured document extraction.
    """
    if provider == "azure":
        if not endpoint or not key:
            raise ValueError("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY must be set")
        return DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    elif provider == "google":
        if not processor_id or not location or not project_id:
            raise ValueError("GOOGLE_DOCUMENT_AI_PROCESSOR_ID, GOOGLE_DOCUMENT_AI_LOCATION, and GOOGLE_CLOUD_PROJECT_ID must be set")
        return documentai.DocumentProcessorServiceClient.from_service_account_file(
            os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")
        )
    else:
        raise ValueError(f"Unsupported provider: {provider}")