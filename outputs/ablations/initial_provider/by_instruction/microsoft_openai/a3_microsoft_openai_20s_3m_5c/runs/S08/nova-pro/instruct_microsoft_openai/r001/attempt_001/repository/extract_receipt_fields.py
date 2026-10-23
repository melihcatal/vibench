import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult

# Initialize the client
client = DocumentIntelligenceClient(
    endpoint=os.getenv('DOCUMENT_INTELLIGENCE_ENDPOINT'),
    credential=os.getenv('DOCUMENT_INTELLIGENCE_KEY')
)

def extract_receipt_fields(receipt_path):
    with open(receipt_path, 'rb') as receipt_data:
        poller = client.begin_analyze_document('prebuilt-receipt', receipt_data)
        result = poller.result()
        fields = {}
        if result.documents:
            doc = result.documents[0]
            fields['merchant'] = doc.fields.get('MerchantName', {}).value
            fields['tax'] = doc.fields.get('Tax', {}).value
            fields['total'] = doc.fields.get('Total', {}).value
            fields['items'] = [{'description': li.value, 'amount': li.amount} for li in doc.fields.get('Items', {}).value]
        return fields