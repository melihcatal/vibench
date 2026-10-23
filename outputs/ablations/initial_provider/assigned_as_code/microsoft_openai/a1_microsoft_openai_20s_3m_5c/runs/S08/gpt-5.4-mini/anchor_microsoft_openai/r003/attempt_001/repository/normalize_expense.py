from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

from document_models import normalize_expense_record


def normalize_expense(payload, config=None):
    config = config or {}
    with DocumentIntelligenceClient(config['endpoint'], AzureKeyCredential(config['api_key'])) as client:
        result = client.begin_analyze_document('prebuilt-document',
            body=payload['document_bytes'], content_type=payload['mime_type']).result()
    fields = result.documents[0].fields if result.documents else {}
    normalized = normalize_expense_record({
        'vendor': fields.get('VendorName').content if fields and 'VendorName' in fields else None,
        'date': fields.get('InvoiceDate').content if fields and 'InvoiceDate' in fields else None,
        'total': fields.get('InvoiceTotal').content if fields and 'InvoiceTotal' in fields else None,
        'tax': fields.get('TotalTax').content if fields and 'TotalTax' in fields else None,
        'items': [],
    })
    return {'normalized_expense': normalized}
