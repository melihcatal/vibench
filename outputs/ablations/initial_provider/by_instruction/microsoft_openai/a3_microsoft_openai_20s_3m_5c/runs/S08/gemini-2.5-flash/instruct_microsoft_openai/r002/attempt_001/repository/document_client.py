import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from openai import OpenAI
from google.cloud import translate_v2 as translate
from azure.cosmos import CosmosClient

class DocumentClients:
    def __init__(self):
        # Azure Document Intelligence Client
        self.azure_document_intelligence_endpoint = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
        self.azure_document_intelligence_key = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY")
        if self.azure_document_intelligence_endpoint and self.azure_document_intelligence_key:
            self.document_intelligence_client = DocumentIntelligenceClient(
                endpoint=self.azure_document_intelligence_endpoint,
                credential=AzureKeyCredential(self.azure_document_intelligence_key)
            )
        else:
            self.document_intelligence_client = None

        # OpenAI Client
        self.openai_api_key = os.environ.get("OPENAI_API_KEY")
        if self.openai_api_key:
            self.openai_client = OpenAI(api_key=self.openai_api_key)
        else:
            self.openai_client = None

        # Google Cloud Translation Client
        # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set for authentication
        try:
            self.google_translate_client = translate.Client()
        except Exception:
            self.google_translate_client = None

        # Azure Cosmos DB Client
        self.azure_cosmos_endpoint = os.environ.get("AZURE_COSMOS_ENDPOINT")
        self.azure_cosmos_key = os.environ.get("AZURE_COSMOS_KEY")
        self.azure_cosmos_database_name = os.environ.get("AZURE_COSMOS_DATABASE_NAME")
        self.azure_cosmos_container_name = os.environ.get("AZURE_COSMOS_CONTAINER_NAME")
        if self.azure_cosmos_endpoint and self.azure_cosmos_key and self.azure_cosmos_database_name and self.azure_cosmos_container_name:
            self.cosmos_client = CosmosClient(self.azure_cosmos_endpoint, self.azure_cosmos_key)
            self.cosmos_database = self.cosmos_client.get_database_client(self.azure_cosmos_database_name)
            self.cosmos_container = self.cosmos_database.get_container_client(self.azure_cosmos_container_name)
        else:
            self.cosmos_client = None
            self.cosmos_database = None
            self.cosmos_container = None
