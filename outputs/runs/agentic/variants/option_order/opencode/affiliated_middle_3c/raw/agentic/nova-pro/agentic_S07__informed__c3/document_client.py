import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


class DocumentClient:
    def __init__(self):
        self.endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
        self.key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")
        self.client = DocumentIntelligenceClient(
            self.endpoint, AzureKeyCredential(self.key)
        )
