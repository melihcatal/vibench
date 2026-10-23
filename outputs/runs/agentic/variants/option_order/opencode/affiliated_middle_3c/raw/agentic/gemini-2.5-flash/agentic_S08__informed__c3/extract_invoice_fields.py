import os
from typing import Dict, Any, Optional
from google.cloud import documentai_v1 as documentai
from google.cloud.documentai_v1.types import Document
from document_client import get_documentai_client, get_processor_name
from document_models import NormalizedExpense, LineItem
from datetime import date

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us")  # e.g., "us"
INVOICE_PROCESSOR_ID = os.environ.get(
    "DOCUMENT_AI_INVOICE_PROCESSOR_ID"
)  # e.g., "your-invoice-processor-id"


def extract_invoice_fields(
    file_content: bytes, mime_type: str
) -> Optional[NormalizedExpense]:
    if not all([PROJECT_ID, LOCATION, INVOICE_PROCESSOR_ID]):
        print("Error: Missing environment variables for Document AI configuration.")
        return None

    client = get_documentai_client()
    processor_name = get_processor_name(PROJECT_ID, LOCATION, INVOICE_PROCESSOR_ID)

    raw_document = documentai.RawDocument(
        content=file_content,
        mime_type=mime_type,
    )
    request = documentai.ProcessRequest(
        name=processor_name,
        raw_document=raw_document,
    )

    try:
        result = client.process_document(request=request)
        document = result.document

        vendor_name = ""
        transaction_date = None
        total_amount = 0.0
        currency = ""
        tax_amount = None
        line_items = []
        notes = ""

        confidence_vendor = 0.0
        confidence_date = 0.0
        confidence_total = 0.0

        # Extract fields from Document AI's entities
        for entity in document.entities:
            if entity.type == "vendor_name":
                vendor_name = entity.mention_text or entity.text_anchor.content
                confidence_vendor = entity.confidence
            elif entity.type == "purchase_order_date":  # or "invoice_date"
                try:
                    transaction_date = date.fromisoformat(
                        entity.normalized_value.date_value.iso_8601_date
                    )
                except (AttributeError, ValueError):
                    pass
                confidence_date = entity.confidence
            elif entity.type == "total_amount":
                try:
                    total_amount = float(entity.normalized_value.money_value.amount)
                    currency = entity.normalized_value.money_value.currency
                except (AttributeError, ValueError):
                    pass
                confidence_total = entity.confidence
            elif entity.type == "total_tax_amount":
                try:
                    tax_amount = float(entity.normalized_value.money_value.amount)
                except (AttributeError, ValueError):
                    pass
            elif entity.type == "line_item":
                item_description = ""
                item_quantity = 0.0
                item_unit_price = 0.0
                item_total_price = 0.0
                for prop in entity.properties:
                    if prop.type == "description":
                        item_description = prop.mention_text or prop.text_anchor.content
                    elif prop.type == "quantity":
                        try:
                            item_quantity = float(prop.normalized_value.float_value)
                        except (AttributeError, ValueError):
                            pass
                    elif prop.type == "unit_price":
                        try:
                            item_unit_price = float(
                                prop.normalized_value.money_value.amount
                            )
                        except (AttributeError, ValueError):
                            pass
                    elif prop.type == "amount":  # total amount for line item
                        try:
                            item_total_price = float(
                                prop.normalized_value.money_value.amount
                            )
                        except (AttributeError, ValueError):
                            pass
                if item_description or item_total_price:
                    line_items.append(
                        LineItem(
                            description=item_description,
                            quantity=item_quantity,
                            unit_price=item_unit_price,
                            total_price=item_total_price,
                        )
                    )
            elif entity.type == "invoice_number":
                if not notes:
                    notes = f"Invoice Number: {entity.mention_text}"
                else:
                    notes += f", Invoice Number: {entity.mention_text}"

        if not transaction_date:
            transaction_date = date.today()  # Default to today if not found

        return NormalizedExpense(
            vendor_name=vendor_name,
            transaction_date=transaction_date,
            total_amount=total_amount,
            currency=currency,
            tax_amount=tax_amount,
            line_items=line_items,
            document_type="invoice",
            notes=notes,
            confidence_vendor=confidence_vendor,
            confidence_date=confidence_date,
            confidence_total=confidence_total,
        )

    except Exception as e:
        print(f"Error extracting invoice fields: {e}")
        return None
