import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

class DocumentClient:
    def __init__(self):
        self.endpoint = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
        self.api_key = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_API_KEY")
        if not self.endpoint or not self.api_key:
            raise ValueError("Azure Document Intelligence endpoint and API key must be set in environment variables.")

    def get_client(self):
        return DocumentIntelligenceClient(self.endpoint, AzureKeyCredential(self.api_key))
