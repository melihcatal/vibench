import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


def extract_text(document_path):
    client = DocumentIntelligenceClient(
        endpoint=os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"),
        credential=AzureKeyCredential(os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")),
    )
    with open(document_path, "rb") as document_file:
        poller = client.begin_analyze_document("prebuilt-document", document_file)
        result = poller.result()
        return result.content
