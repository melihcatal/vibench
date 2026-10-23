import os
from document_client import process_document
from document_models import ExtractedInvoice, ExtractedLineItem

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
LOCATION = "us"
INVOICE_PROCESSOR_ID = os.environ.get("DOCUMENT_AI_INVOICE_PROCESSOR_ID")


def extract_invoice_fields(file_content: bytes, mime_type: str) -> ExtractedInvoice:
    if not PROJECT_ID or not INVOICE_PROCESSOR_ID:
        raise ValueError(
            "GCP_PROJECT_ID and DOCUMENT_AI_INVOICE_PROCESSOR_ID must be set as environment variables."
        )

    document = process_document(
        PROJECT_ID, LOCATION, INVOICE_PROCESSOR_ID, file_content, mime_type
    )

    vendor_name = None
    invoice_date = None
    total_amount = None
    currency = None
    line_items = []
    notes = None

    for entity in document.entities:
        if entity.type_ == "vendor_name":
            vendor_name = entity.mention_text
        elif entity.type_ == "invoice_date":
            invoice_date = entity.mention_text
        elif entity.type_ == "total_amount":
            total_amount = float(entity.mention_text) if entity.mention_text else None
            if entity.currency:  # Prefer structured currency if available
                currency = entity.currency_symbol or entity.currency_code
        elif entity.type_ == "line_item":
            description = None
            quantity = None
            unit_price = None
            total_price = None
            for prop in entity.properties:
                if prop.type_ == "description":
                    description = prop.mention_text
                elif prop.type_ == "quantity":
                    quantity = float(prop.mention_text) if prop.mention_text else None
                elif prop.type_ == "unit_price":
                    unit_price = float(prop.mention_text) if prop.mention_text else None
                elif prop.type_ == "total_price":
                    total_price = (
                        float(prop.mention_text) if prop.mention_text else None
                    )
            line_items.append(
                ExtractedLineItem(
                    description=description,
                    quantity=quantity,
                    unit_price=unit_price,
                    total_price=total_price,
                )
            )
        elif entity.type_ == "notes":
            notes = entity.mention_text

    return ExtractedInvoice(
        vendor_name=vendor_name,
        invoice_date=invoice_date,
        total_amount=total_amount,
        currency=currency,
        line_items=line_items,
        notes=notes,
    )
