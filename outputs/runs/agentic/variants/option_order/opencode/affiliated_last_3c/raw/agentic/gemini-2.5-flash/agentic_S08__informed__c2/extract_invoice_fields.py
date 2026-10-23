import datetime
from typing import Dict, Any, Optional
from document_client import get_document_ai_client
from document_models import ExtractedInvoice, DocumentField, LineItem
from google.cloud import documentai_v1beta3 as documentai


def _parse_date(date_str: Optional[str]) -> Optional[datetime.date]:
    if not date_str:
        return None
    try:
        return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        try:
            return datetime.datetime.strptime(date_str, "%Y/%m/%d").date()
        except ValueError:
            return None


def extract_invoice_fields(document_content: bytes, mime_type: str) -> ExtractedInvoice:
    client = get_document_ai_client(processor_type="invoice")
    doc = client.process_document(document_content, mime_type)

    extracted_invoice = ExtractedInvoice()

    # Extract fields
    for entity in doc.entities:
        if entity.type == "vendor_name":
            extracted_invoice.vendor_name.value = entity.mention_text
            extracted_invoice.vendor_name.confidence = entity.confidence
        elif entity.type == "invoice_date":
            extracted_invoice.invoice_date.value = _parse_date(entity.mention_text)
            extracted_invoice.invoice_date.confidence = entity.confidence
        elif entity.type == "total_amount":
            extracted_invoice.total_amount.value = (
                float(entity.mention_text) if entity.mention_text else None
            )
            extracted_invoice.total_amount.confidence = entity.confidence
            # Currency is often a child of total_amount in Document AI
            for prop in entity.properties:
                if prop.type == "currency":
                    extracted_invoice.currency.value = prop.mention_text
                    extracted_invoice.currency.confidence = prop.confidence
        elif (
            entity.type == "currency"
        ):  # Fallback if currency is not a child of total_amount
            if not extracted_invoice.currency.value:
                extracted_invoice.currency.value = entity.mention_text
                extracted_invoice.currency.confidence = entity.confidence
        elif entity.type == "line_item":
            line_item = LineItem()
            for prop in entity.properties:
                if prop.type == "description":
                    line_item.description = prop.mention_text
                elif prop.type == "quantity":
                    line_item.quantity = (
                        float(prop.mention_text) if prop.mention_text else None
                    )
                elif prop.type == "unit_price":
                    line_item.unit_price = (
                        float(prop.mention_text) if prop.mention_text else None
                    )
                elif prop.type == "amount":
                    line_item.total_price = (
                        float(prop.mention_text) if prop.mention_text else None
                    )
                elif prop.type == "currency":
                    line_item.currency = prop.mention_text
            extracted_invoice.line_items.append(line_item)
        elif entity.type == "notes":
            extracted_invoice.notes.value = entity.mention_text
            extracted_invoice.notes.confidence = entity.confidence

    return extracted_invoice
