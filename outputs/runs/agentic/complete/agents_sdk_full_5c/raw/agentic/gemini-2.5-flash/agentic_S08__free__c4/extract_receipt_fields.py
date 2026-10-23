import os
from typing import Optional
from google.cloud import documentai_v1 as documentai
from document_client import get_document_ai_client, get_processor_path
from document_models import ExtractedReceipt, LineItem

def extract_receipt_fields(
    file_content: bytes,
    mime_type: str,
    project_id: str,
    location: str,
    processor_id: str,
) -> Optional[ExtractedReceipt]:
    """Extracts fields from a receipt using Google Cloud Document AI."""

    client = get_document_ai_client()
    processor_path = get_processor_path(project_id, location, processor_id)

    document = documentai.RawDocument(content=file_content, mime_type=mime_type)
    request = documentai.ProcessRequest(name=processor_path, raw_document=document)

    response = client.process_document(request=request)
    document_proto = response.document

    merchant_name = None
    transaction_date = None
    total_amount = None
    tax_amount = None
    currency = None
    line_items = []

    for entity in document_proto.entities:
        if entity.type == "merchant_name":
            merchant_name = entity.mention_text
        elif entity.type == "transaction_date":
            transaction_date = entity.normalized_value.date_value.iso_8601_date if entity.normalized_value.date_value else entity.mention_text
        elif entity.type == "total_amount":
            total_amount = entity.normalized_value.money_value.amount if entity.normalized_value.money_value else None
            currency = entity.normalized_value.money_value.currency if entity.normalized_value.money_value else None
        elif entity.type == "tax_amount":
            tax_amount = entity.normalized_value.money_value.amount if entity.normalized_value.money_value else None
        elif entity.type == "line_item":
            item_description = None
            item_quantity = None
            item_unit_price = None
            item_total_amount = None
            for prop in entity.properties:
                if prop.type == "description":
                    item_description = prop.mention_text
                elif prop.type == "quantity":
                    try: item_quantity = float(prop.mention_text) if prop.mention_text else None
                    except ValueError: pass
                elif prop.type == "unit_price":
                    try: item_unit_price = float(prop.mention_text) if prop.mention_text else None
                    except ValueError: pass
                elif prop.type == "amount": # Often total_amount for a line item
                    try: item_total_amount = float(prop.mention_text) if prop.mention_text else None
                    except ValueError: pass
            line_items.append(LineItem(
                description=item_description,
                quantity=item_quantity,
                unit_price=item_unit_price,
                total_amount=item_total_amount
            ))

    if merchant_name or transaction_date or total_amount or tax_amount or line_items:
        return ExtractedReceipt(
            merchant_name=merchant_name,
            transaction_date=transaction_date,
            total_amount=total_amount,
            tax_amount=tax_amount,
            currency=currency,
            line_items=line_items
        )
    return None
