import os
from typing import Optional

from google.cloud import documentai_v1 as documentai

from document_client import process_document_with_documentai
from document_models import ExtractedReceiptFields, LineItem

def extract_receipt_fields(
    file_content: bytes,
    mime_type: str,
    project_id: Optional[str] = None,
    location: Optional[str] = None,
    processor_id: Optional[str] = None,
) -> ExtractedReceiptFields:
    """Extracts merchant, tax, total, and items from a receipt using Google Document AI."""

    # Use environment variables for configuration
    project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    location = location or os.environ.get("GOOGLE_CLOUD_LOCATION", "us")
    processor_id = processor_id or os.environ.get("GOOGLE_DOCUMENTAI_RECEIPT_PROCESSOR_ID")

    if not all([project_id, location, processor_id]):
        raise ValueError(
            "Google Cloud Project ID, Location, and Document AI Receipt Processor ID "
            "must be provided either as arguments or environment variables."
        )

    document = process_document_with_documentai(
        project_id=project_id,
        location=location,
        processor_id=processor_id,
        file_content=file_content,
        mime_type=mime_type,
    )

    merchant_name = None
    transaction_date = None
    total_amount = None
    currency = None
    tax_amount = None
    line_items: list[LineItem] = []

    for entity in document.entities:
        if entity.type == "merchant_name":
            merchant_name = entity.mention_text
        elif entity.type == "transaction_date":
            transaction_date = entity.mention_text
        elif entity.type == "total_amount":
            if entity.money_value and entity.money_value.units is not None:
                total_amount = float(f"{entity.money_value.units}.{entity.money_value.nanos:09d}")
                currency = entity.money_value.currency_code
            elif entity.mention_text:
                try:
                    total_amount = float(entity.mention_text)
                except ValueError:
                    pass
        elif entity.type == "sub_total" or entity.type == "tax_amount": # Google Document AI often labels tax as sub_total for receipts
            if entity.money_value and entity.money_value.units is not None:
                tax_amount = float(f"{entity.money_value.units}.{entity.money_value.nanos:09d}")

        elif entity.type == "line_item":
            description = None
            quantity = None
            unit_price = None
            total_price = None
            for sub_entity in entity.properties:
                if sub_entity.type == "description":
                    description = sub_entity.mention_text
                elif sub_entity.type == "quantity" and sub_entity.mention_text:
                    try:
                        quantity = float(sub_entity.mention_text)
                    except ValueError:
                        pass
                elif sub_entity.type == "unit_price" and sub_entity.money_value and sub_entity.money_value.units is not None:
                    unit_price = float(f"{sub_entity.money_value.units}.{sub_entity.money_value.nanos:09d}")
                elif sub_entity.type == "line_item_amount" and sub_entity.money_value and sub_entity.money_value.units is not None:
                    total_price = float(f"{sub_entity.money_value.units}.{sub_entity.money_value.nanos:09d}")

            line_items.append(
                LineItem(
                    description=description if description is not None else "",
                    quantity=quantity,
                    unit_price=unit_price,
                    total_price=total_price,
                )
            )

    return ExtractedReceiptFields(
        merchant_name=merchant_name,
        transaction_date=transaction_date,
        total_amount=total_amount,
        currency=currency,
        tax_amount=tax_amount,
        line_items=line_items,
    )
