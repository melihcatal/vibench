from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
import os

# Set up the client
endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")
client = DocumentIntelligenceClient(endpoint, AzureKeyCredential(key))


def extract_structured_fields(document_path):
    with open(document_path, "rb") as document_file:
        poller = client.begin_analyze_document("prebuilt-document", document_file)
        result = poller.result()
        return result.fields
