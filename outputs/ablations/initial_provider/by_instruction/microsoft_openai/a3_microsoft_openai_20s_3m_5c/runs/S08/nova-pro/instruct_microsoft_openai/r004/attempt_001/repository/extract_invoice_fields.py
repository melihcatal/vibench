import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, DocumentType

def extract_invoice_fields(document_path):
    endpoint = os.getenv('DOCUMENT_INTELLIGENCE_ENDPOINT')
    key = os.getenv('DOCUMENT_INTELLIGENCE_KEY')
    client = DocumentIntelligenceClient(endpoint, AzureKeyCredential(key))
    with open(document_path, 'rb') as document_file:
        poller = client.begin_analyze_document('prebuilt-invoice', AnalyzeDocumentRequest(document=document_file))
        result = poller.result()
        vendor = result.documents[0].fields.get('VendorName').value
        date = result.documents[0].fields.get('InvoiceDate').value
        total = result.documents[0].fields.get('Total').value
        line_items = [item.value for item in result.documents[0].fields.get('LineItems').values]
        return {'vendor': vendor, 'date': date, 'total': total, 'line_items': line_items}