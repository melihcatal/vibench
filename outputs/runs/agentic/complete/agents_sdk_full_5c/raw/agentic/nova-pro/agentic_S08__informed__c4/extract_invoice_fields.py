import os
from google.cloud import documentai

def extract_invoice_fields(invoice_path):
    client = documentai.DocumentProcessorServiceClient()
    gcs_source_uri = f"gs://{os.getenv('GOOGLE_CLOUD_PROJECT')}/{invoice_path}"
    request = documentai.ProcessRequest(name=os.getenv('DOCUMENT_AI_PROJECT_ID'), gcs_source=documentai.GcsSource(uris=[gcs_source_uri]))
    result = client.process_document(request)
    document = result.document
    vendor = document.fields['vendor'].value_string
    date = document.fields['date'].value_date
    total = document.fields['total'].value_money
    line_items = [item.value_string for item in document.fields['line_items'].array_value.values]
    return {'vendor': vendor, 'date': date, 'total': total, 'line_items': line_items}