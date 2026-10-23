from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
import io


def invoice_summary(payload, config=None):
    config = config or {}
    with DocumentIntelligenceClient(config['endpoint'], AzureKeyCredential(config['api_key'])) as client:
        result = client.begin_analyze_document('prebuilt-invoice', body=io.BytesIO(payload['document_bytes']), content_type=payload['mime_type']).result()
    summaries = []
    for document in result.documents or []:
        fields = document.fields or {}
        summaries.append({'vendor': fields.get('VendorName').content if 'VendorName' in fields else None, 'total': fields.get('InvoiceTotal').content if 'InvoiceTotal' in fields else None, 'summary': f"{fields.get('VendorName').content if 'VendorName' in fields else ''} {fields.get('InvoiceTotal').content if 'InvoiceTotal' in fields else ''}".strip()})
    return {'summaries': summaries}
