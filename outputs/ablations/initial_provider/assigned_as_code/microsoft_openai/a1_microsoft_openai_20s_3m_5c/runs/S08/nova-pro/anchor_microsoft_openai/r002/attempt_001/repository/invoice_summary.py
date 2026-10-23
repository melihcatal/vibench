import io
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


def summarize_invoice(payload, config=None):
    config = config or {}
    with DocumentIntelligenceClient(config['endpoint'], AzureKeyCredential(config['api_key'])) as client:
        result = client.begin_analyze_document('prebuilt-invoice',
            body=io.BytesIO(payload['document_bytes']), content_type=payload['mime_type']).result()
        invoice = result.documents[0]
        summary = {
            'vendor': invoice.fields.get('VendorName').content,
            'date': invoice.fields.get('InvoiceDate').content,
            'total': invoice.fields.get('InvoiceTotal').content
        }
        return summary