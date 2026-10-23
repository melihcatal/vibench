import os
from typing import Dict, Any, List, Optional
from google.cloud import documentai_v1 as documentai
from document_client import get_documentai_client, get_processor_name
from document_models import DocumentExtractionResult, LineItem

def extract_invoice_fields(image_content: bytes) -> DocumentExtractionResult:
    client, project_id, location = get_documentai_client()
    processor_id = os.environ.get("GOOGLE_CLOUD_DOCUMENTAI_INVOICE_PROCESSOR_ID")

    if not processor_id:
        raise ValueError("GOOGLE_CLOUD_DOCUMENTAI_INVOICE_PROCESSOR_ID environment variable not set.")

    processor_name = get_processor_name(project_id, location, processor_id)

    raw_document = documentai.RawDocument(content=image_content, mime_type="application/pdf")
    request = documentai.ProcessRequest(name=processor_name, raw_document=raw_document)

    result = client.process_document(request=request)
    document = result.document

    vendor_name: Optional[str] = None
    document_date: Optional[str] = None
    total_amount: Optional[float] = None
    line_items: List[LineItem] = []

    for entity in document.entities:
        if entity.type == "vendor_name":
            vendor_name = entity.mention_text
        elif entity.type == "document_date":
            document_date = entity.mention_text
        elif entity.type == "total_amount":
            try:
                total_amount = float(entity.mention_text)
            except (ValueError, TypeError):
                total_amount = None
        elif entity.type == "line_item":
            description: Optional[str] = None
            quantity: Optional[float] = None
            unit_price: Optional[float] = None
            total_price: Optional[float] = None
            for prop in entity.properties:
                if prop.type == "description":
                    description = prop.mention_text
                elif prop.type == "quantity":
                    try:
                        quantity = float(prop.mention_text)
                    except (ValueError, TypeError):
                        quantity = None
                elif prop.type == "unit_price":
                    try:
                        unit_price = float(prop.mention_text)
                    except (ValueError, TypeError):
                        unit_price = None
                elif prop.type == "amount": # Document AI often uses 'amount' for line item total
                    try:
                        total_price = float(prop.mention_text)
                    except (ValueError, TypeError):
                        total_price = None
            line_items.append(LineItem(description=description, quantity=quantity, unit_price=unit_price, total_price=total_price))

    return DocumentExtractionResult(
        vendor_name=vendor_name,
        document_date=document_date,
        total_amount=total_amount,
        line_items=line_items,
        raw_response=document.to_dict() # Convert Document object to dictionary for raw_response
    )
