import os
from google.cloud import documentai

# Configure client using environment variable
client = documentai.DocumentProcessorServiceClient()
project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
processor_id = os.getenv("RECEIPT_PROCESSOR_ID")  # e.g., "projects/{project_id}/locations/{location}/processors/{processor}"

def extract_receipt_fields(document_bytes):
    """Use Google Document AI Receipt parser to extract merchant, tax, total, and items.
    Returns a dict with keys: merchant, tax, total, items (list of dicts).
    """
    name = processor_id
    with client.process_document(parent=name, document=document_bytes) as response:
        entities = response.document.entities
        merchant = next((e for e in entities if e.type == 'MERCHANT'), None)
        tax = next((e for e in entities if e.type == 'TAX'), None)
        total = next((e for e in entities if e.type == 'TOTAL'), None)
        items = [e for e in entities if e.type == 'ITEM']
        result = {
            "merchant": merchant.text if merchant else None,
            "tax": tax.text if tax else None,
            "total": total.text if total else None,
            "items": [
                {
                    "description": it.text,
                    "price": it.properties.get('price', {}).get('text')
                } for it in items
            ]
        }
        return result
