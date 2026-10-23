import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, DocumentType

def extract_receipt_fields(document_path):
    endpoint = os.getenv('DOCUMENT_INTELLIGENCE_ENDPOINT')
    key = os.getenv('DOCUMENT_INTELLIGENCE_KEY')
    client = DocumentIntelligenceClient(endpoint, AzureKeyCredential(key))
    with open(document_path, 'rb') as document_file:
        poller = client.begin_analyze_document('prebuilt-receipt', AnalyzeDocumentRequest(document=document_file))
        result = poller.result()
        merchant = result.documents[0].fields.get('MerchantName').value
        tax = result.documents[0].fields.get('Tax').value
        total = result.documents[0].fields.get('Total').value
        items = [item.value for item in result.documents[0].fields.get('Items').values]
        return {'merchant': merchant, 'tax': tax, 'total': total, 'items': items}