from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

def stored_document_ocr(document_url):
    endpoint = 'https://{your-resource-name}.cognitiveservices.azure.com/'
    key = '{your-api-key}'
    client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    poller = client.begin_analyze_document('prebuilt-document', document_url=document_url)
    result = poller.result()
    return result