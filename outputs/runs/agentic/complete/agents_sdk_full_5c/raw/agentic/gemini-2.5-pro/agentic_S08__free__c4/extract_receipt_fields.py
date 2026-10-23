# extract_receipt_fields.py
import os
from document_client import get_google_document_ai_client
from document_models import ExtractedReceipt, ReceiptLineItem
from google.cloud import documentai

def extract_receipt_from_file(file_path: str, mime_type: str = "application/pdf") -> ExtractedReceipt:
    """
    Extracts structured data from a receipt document using Google Cloud Document AI.
    """
    client = get_google_document_ai_client()
    
    project_id = os.environ.get("GCP_PROJECT_ID")
    location = os.environ.get("GCP_LOCATION")
    processor_id = os.environ.get("GCP_PROCESSOR_ID") # Specific for receipts
    
    name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_document(request=request)
    doc = result.document

    entities = {entity.type_: entity.mention_text for entity in doc.entities}

    items = []
    if 'line_item' in entities:
         for item_entity in doc.entities:
             if item_entity.type_ == 'line_item':
                items.append(ReceiptLineItem(
                    description=item_entity.mention_text, # Simplified for example
                    quantity=None, # Not always available in a structured way
                    price=None
                ))

    return ExtractedReceipt(
        merchant_name=entities.get("supplier_name"),
        transaction_date=entities.get("receipt_date"),
        total_amount=float(entities.get("total_amount", 0.0)),
        tax_amount=float(entities.get("total_tax_amount", 0.0)),
        items=items,
        raw_fields={e.type_: {"value": e.mention_text, "confidence": e.confidence} for e in doc.entities}
    )
