import os
from google.cloud import documentai

# Configure client using environment variable
client = documentai.DocumentProcessorServiceClient()
project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
processor_id = os.getenv("INVOICE_PROCESSOR_ID")  # e.g., "projects/{project_id}/locations/{location}/processors/{processor}"

def extract_invoice_fields(document_bytes):
    """Use Google Document AI Invoice parser to extract vendor, date, total, and line items.
    Returns a dict with keys: vendor, invoice_date, total, line_items (list of dicts).
    """
    name = processor_id
    with client.process_document(parent=name, document=document_bytes) as response:
        # Assume the processor returns entities with types for vendor, date, total, and line items
        entities = response.document.entities
        vendor = next((e for e in entities if e.type == 'VENDOR'), None)
        invoice_date = next((e for e in entities if e.type == 'DATE'), None)
        total = next((e for e in entities if e.type == 'TOTAL'), None)
        line_items = [e for e in entities if e.type == 'LINE_ITEM']
        result = {
            "vendor": vendor.text if vendor else None,
            "invoice_date": invoice_date.text if invoice_date else None,
            "total": total.text if total else None,
            "line_items": [
                {
                    "description": li.text,
                    "quantity": li.properties.get('quantity', {}).get('text'),
                    "unit_price": li.properties.get('unit_price', {}).get('text')
                } for li in line_items
            ]
        }
        return result
