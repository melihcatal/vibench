import os
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

def extract_invoice_fields(invoice_path):
    endpoint = os.getenv('FORM_RECOGNIZER_ENDPOINT')
    key = os.getenv('FORM_RECOGNIZER_KEY')
    client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    with open(invoice_path, "rb") as f:
        poller = client.begin_analyze_document('prebuilt-invoice', document=f)
        result = poller.result()
        invoice_fields = {
            'vendor': result.fields.get('VendorName').value,
            'date': result.fields.get('VendorName').value,
            'total': result.fields.get('Total').value,
            'line_items': [{'description': item.value.get('Description').value, 'amount': item.value.get('Amount').value} for item in result.fields.get('Items').values()]
        }
        return invoice_fields