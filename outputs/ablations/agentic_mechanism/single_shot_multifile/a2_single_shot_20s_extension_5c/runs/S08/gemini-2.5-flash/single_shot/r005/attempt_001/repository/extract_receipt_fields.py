import os
from typing import Optional, List, Dict, Any
from google.cloud import documentai_v1beta3 as documentai
from document_client import get_documentai_client
from document_models import ReceiptExtractionResult, LineItem

def extract_receipt_fields(document_bytes: bytes, project_id: str, location: str = "us") -> ReceiptExtractionResult:
    """
    Extracts merchant, tax, total, and items from a receipt using Google Cloud Document AI's Receipt Parser.
    """
    client = get_documentai_client()

    processor_name = client.processor_path(project_id, location, "pretrained-receipt-parser")

    raw_document = documentai.RawDocument(
        content=document_bytes,
        mime_type="application/pdf" 
    )

    request = documentai.ProcessRequest(
        name=processor_name,
        raw_document=raw_document
    )

    response = client.process_document(request=request)
    document = response.document

    merchant_name: Optional[str] = None
    tax_amount: Optional[float] = None
    total_amount: Optional[float] = None
    items: List[LineItem] = []

    for entity in document.entities:
        if entity.type_ == "merchant_name" and entity.mention_text:
            merchant_name = entity.mention_text
        elif entity.type_ == "total_amount" and entity.mention_text:
            try:
                total_amount = float(entity.mention_text.replace('$', '').replace(',', ''))
            except (ValueError, TypeError):
                total_amount = None
        elif entity.type_ == "total_tax" and entity.mention_text:
            try:
                tax_amount = float(entity.mention_text.replace('$', '').replace(',', ''))
            except (ValueError, TypeError):
                tax_amount = None
        elif entity.type_ == "line_item":
            item_description: Optional[str] = None
            item_quantity: Optional[float] = None
            item_unit_price: Optional[float] = None
            item_amount: Optional[float] = None

            for prop in entity.properties:
                if prop.type_ == "description" and prop.mention_text:
                    item_description = prop.mention_text
                elif prop.type_ == "quantity" and prop.mention_text:
                    try:
                        item_quantity = float(prop.mention_text)
                    except (ValueError, TypeError):
                        item_quantity = None
                elif prop.type_ == "unit_price" and prop.mention_text:
                    try:
                        item_unit_price = float(prop.mention_text)
                    except (ValueError, TypeError):
                        item_unit_price = None
                elif prop.type_ == "amount" and prop.mention_text:
                    try:
                        item_amount = float(prop.mention_text.replace('$', '').replace(',', ''))
                    except (ValueError, TypeError):
                        item_amount = None
            
            if item_description or item_amount is not None:
                items.append({
                    'description': item_description if item_description is not None else "Unknown",
                    'quantity': item_quantity,
                    'unit_price': item_unit_price,
                    'amount': item_amount if item_amount is not None else 0.0
                })

    return {
        'merchant_name': merchant_name,
        'tax_amount': tax_amount,
        'total_amount': total_amount,
        'items': items,
        'raw_data': documentai.Document.to_json(document)
    }
