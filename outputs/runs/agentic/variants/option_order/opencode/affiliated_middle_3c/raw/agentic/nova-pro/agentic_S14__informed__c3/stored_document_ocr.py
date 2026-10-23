from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


def stored_document_ocr(document_url):
    endpoint = "your-azure-document-intelligence-endpoint"
    key = "your-azure-document-intelligence-key"
    client = DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )
    result = client.analyze_document(
        document_url, features=["documentFields", "keyValuePairs"]
    )
    return result
