from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

client = DocumentIntelligenceClient(
    endpoint=os.getenv('AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT'),
    credential=AzureKeyCredential(os.getenv('AZURE_DOCUMENT_INTELLIGENCE_KEY'))
)

def stored_document_ocr(document_path):
    with open(document_path, 'rb') as document_data:
        poller = client.begin_analyze_document('prebuilt-document', document_data)
        result = poller.result()
        return result