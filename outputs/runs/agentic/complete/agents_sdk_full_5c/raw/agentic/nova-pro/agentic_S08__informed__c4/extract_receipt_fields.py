import os
from google.cloud import documentai

def extract_receipt_fields(receipt_path):
    client = documentai.DocumentProcessorServiceClient()
    gcs_source_uri = f"gs://{os.getenv('GOOGLE_CLOUD_PROJECT')}/{receipt_path}"
    request = documentai.ProcessRequest(name=os.getenv('DOCUMENT_AI_PROJECT_ID'), gcs_source=documentai.GcsSource(uris=[gcs_source_uri]))
    result = client.process_document(request)
    document = result.document
    merchant = document.fields['merchant'].value_string
    tax = document.fields['tax'].value_money
    total = document.fields['total'].value_money
    items = [item.value_string for item in document.fields['items'].array_value.values]
    return {'merchant': merchant, 'tax': tax, 'total': total, 'items': items}