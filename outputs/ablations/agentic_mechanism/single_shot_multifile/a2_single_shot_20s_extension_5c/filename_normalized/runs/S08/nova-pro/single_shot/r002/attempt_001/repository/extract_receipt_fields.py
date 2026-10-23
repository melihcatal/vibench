import os
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

def extract_receipt_fields(receipt_path):
    endpoint = os.getenv('FORM_RECOGNIZER_ENDPOINT')
    key = os.getenv('FORM_RECOGNIZER_KEY')
    client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    with open(receipt_path, "rb") as f:
        poller = client.begin_analyze_document('prebuilt-receipt', document=f)
        result = poller.result()
        receipt_fields = {
            'merchant': result.fields.get('MerchantName').value,
            'tax': result.fields.get('Tax').value,
            'total': result.fields.get('Total').value,
            'items': [{'description': item.value.get('Description').value, 'amount': item.value.get('Amount').value} for item in result.fields.get('Items').values()]
        }
        return receipt_fields