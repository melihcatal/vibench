from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
import io


def normalize_expense(payload, config=None):
    config = config or {}
    with DocumentIntelligenceClient(config['endpoint'], AzureKeyCredential(config['api_key'])) as client:
        result = client.begin_analyze_document('prebuilt-document', body=io.BytesIO(payload['document_bytes']), content_type=payload['mime_type']).result()
    documents = []
    for document in result.documents or []:
        fields = document.fields or {}
        documents.append({'vendor': fields.get('VendorName').content if 'VendorName' in fields else None, 'date': fields.get('InvoiceDate').content if 'InvoiceDate' in fields else None, 'total': fields.get('InvoiceTotal').content if 'InvoiceTotal' in fields else None, 'currency': fields.get('TransactionCurrency').content if 'TransactionCurrency' in fields else None})
    return {'expenses': documents}
