from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


def invoice_summary(payload, config=None):
    config = config or {}
    with DocumentIntelligenceClient(config['endpoint'], AzureKeyCredential(config['api_key'])) as client:
        result = client.begin_analyze_document('prebuilt-invoice', body=payload['document_bytes'], content_type=payload['mime_type']).result()
    summaries = []
    for document in result.documents or []:
        fields = document.fields or {}
        vendor = fields['VendorName'].content if 'VendorName' in fields else None
        invoice_date = fields['InvoiceDate'].content if 'InvoiceDate' in fields else None
        total = fields['InvoiceTotal'].content if 'InvoiceTotal' in fields else None
        summaries.append({'summary': f'{vendor} invoice on {invoice_date} totals {total}' if vendor or invoice_date or total else None})
    return {'summaries': summaries}
