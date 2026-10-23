import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from google.cloud import documentai_v1 as documentai
from google.oauth2 import service_account


def get_document_intelligence_client() -> DocumentIntelligenceClient:
    endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")
    return DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))


def get_document_ai_client() -> documentai.DocumentAIClient:
    credentials = service_account.Credentials.from_service_account_file(
        os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    )
    return documentai.DocumentAIClient(credentials=credentials)