from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


def invoice_summary(payload, config=None):
    config = config or {}
    with DocumentIntelligenceClient(config['endpoint'], AzureKeyCredential(config['api_key'])) as client:
        result = client.begin_analyze_document('prebuilt-invoice',
            body=payload['document_bytes'], content_type=payload['mime_type']).result()
    return {'summary': [{'vendor': (doc.fields or {}).get('VendorName').content if (doc.fields or {}) and 'VendorName' in (doc.fields or {}) else None,
                         'total': (doc.fields or {}).get('InvoiceTotal').content if (doc.fields or {}) and 'InvoiceTotal' in (doc.fields or {}) else None} for doc in result.documents or []]}
