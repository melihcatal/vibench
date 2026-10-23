import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult

# Initialize the client
client = DocumentIntelligenceClient(
    endpoint=os.getenv('DOCUMENT_INTELLIGENCE_ENDPOINT'),
    credential=os.getenv('DOCUMENT_INTELLIGENCE_KEY')
)

def extract_invoice_fields(invoice_path):
    with open(invoice_path, 'rb') as invoice_data:
        poller = client.begin_analyze_document('prebuilt-invoice', invoice_data)
        result = poller.result()
        fields = {}
        if result.documents:
            doc = result.documents[0]
            fields['vendor'] = doc.fields.get('VendorName', {}).value
            fields['date'] = doc.fields.get('VendorInvoiceDate', {}).value
            fields['total'] = doc.fields.get('Total', {}).value
            fields['line_items'] = [{'description': li.value, 'amount': li.amount} for li in doc.fields.get('LineItems', {}).value]
        return fields