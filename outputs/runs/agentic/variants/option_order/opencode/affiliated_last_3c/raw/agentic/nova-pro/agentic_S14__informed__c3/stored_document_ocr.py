import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

def stored_document_ocr(document_path):
    endpoint = os.getenv('AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT')
    key = os.getenv('AZURE_DOCUMENT_INTELLIGENCE_KEY')
    client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    with open(document_path, "rb") as document_file:
        poller = client.begin_analyze_document("prebuilt-document", document_file)
        result = poller.result()
        for idx, document in enumerate(result.documents):
            print("Document #{} has {} pages.".