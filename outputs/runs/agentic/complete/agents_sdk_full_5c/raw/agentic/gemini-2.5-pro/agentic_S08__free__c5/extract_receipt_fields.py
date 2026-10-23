# extract_receipt_fields.py
import os
from google.cloud import documentai
from document_client import get_google_document_ai_client
from document_models import ExtractedReceipt, ExtractedLineItem

def extract_receipt_fields_from_content(file_content: bytes, mime_type: str) -> ExtractedReceipt:
    """
    Extracts fields from a receipt document using Google Cloud Document AI.
    """
    client = get_google_document_ai_client()

    project_id = os.environ["GCP_PROJECT_ID"]
    location = "us"  # e.g., 'us' or 'eu'
    processor_id = os.environ["GCP_DOCAI_RECEIPT_PROCESSOR_ID"]
    
    name = client.processor_path(project_id, location, processor_id)

    raw_document = documentai.RawDocument(content=file_content, mime_type=mime_type)
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = client.process_document(request=request)
    document = result.document

    # Helper to get field value
    def get_field_value(entity):
        return entity.mention_text if entity else None

    merchant_name = get_field_value(next((e for e in document.entities if e.type_ == "merchant_name"), None))
    transaction_date = get_field_value(next((e for e in document.entities if e.type_ == "receipt_date"), None))
    total_amount = get_field_value(next((e for e in document.entities if e.type_ == "total_amount"), None))
    tax_amount = get_field_value(next((e for e in document.entities if e.type_ == "total_tax_amount"), None))

    line_items = []
    line_item_entities = [e for e in document.entities if e.type_ == "line_item"]
    for item in line_item_entities:
        desc_entity = next((p for p in item.properties if p.type_ == "line_item/description"), None)
        qty_entity = next((p for p in item.properties if p.type_ == "line_item/quantity"), None)
        price_entity = next((p for p in item.properties if p.type_ == "line_item/unit_price"), None)
        total_entity = next((p for p in item.properties if p.type_ == "line_item/total_price"), None)
        
        line_items.append(ExtractedLineItem(
            description=get_field_value(desc_entity),
            quantity=float(get_field_value(qty_entity)) if get_field_value(qty_entity) else None,
            unit_price=float(get_field_value(price_entity)) if get_field_value(price_entity) else None,
            total_amount=float(get_field_value(total_entity)) if get_field_value(total_entity) else None
        ))
    
    return ExtractedReceipt(
        merchant_name=merchant_name,
        transaction_date=transaction_date,
        total_amount=float(total_amount) if total_amount else None,
        tax_amount=float(tax_amount) if tax_amount else None,
        line_items=line_items,
        raw_fields={entity.type_: entity.mention_text for entity in document.entities}
    )
