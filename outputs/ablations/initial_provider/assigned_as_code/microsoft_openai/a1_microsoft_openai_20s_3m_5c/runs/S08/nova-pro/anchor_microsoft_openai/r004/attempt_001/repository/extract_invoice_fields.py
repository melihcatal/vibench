import io
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


def extract_invoice_fields(payload, config=None):
    config = config or {}
    with DocumentIntelligenceClient(config['endpoint'], AzureKeyCredential(config['api_key'])) as client:
        result = client.begin_analyze_document('prebuilt-invoice',
            body=io.BytesIO(payload['document_bytes']), content_type=payload['mime_type']).result()
    invoices = []
    for document in result.documents or []:
        fields = document.fields or {}
        text = lambda values, key: values[key].content if key in values else None
        items = fields.get('Items')
        lines = []
        for item in (items.value_array or []) if items else []:
            values = item.value_object or {}
            lines.append({'description': text(values, 'Description'), 'quantity': text(values, 'Quantity'),
                          'amount': text(values, 'Amount')})
        invoices.append({'vendor': text(fields, 'VendorName'), 'date': text(fields, 'InvoiceDate'),
                         'total': text(fields, 'InvoiceTotal'), 'line_items': lines})
    return {'invoices': invoices}
