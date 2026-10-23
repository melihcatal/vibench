import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

def stored_document_ocr(blob_content):
    endpoint = os.getenv('AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT')
    key = os.getenv('AZURE_DOCUMENT_INTELLIGENCE_KEY')
    client = DocumentIntelligenceClient(endpoint, AzureKeyCredential(key))
    poller = client.begin_analyze_document('prebuilt-document', blob_content)
    result = poller.result()
    print(result)
    return result

if __name__ == '__main__':\n    with open('local/path/to/file.pdf', 'rb') as f:\n        blob_content = f.read()\n        stored_document_ocr(blob_content)