import datetime
from typing import Dict, Any, Optional
from document_client import get_document_ai_client
from document_models import ExtractedReceipt, DocumentField, LineItem
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


def extract_receipt_fields(document_content: bytes, mime_type: str) -> ExtractedReceipt:
    client = get_document_ai_client(processor_type="receipt")
    doc = client.process_document(document_content, mime_type)

    extracted_receipt = ExtractedReceipt()

    for entity in doc.entities:
        if entity.type == "merchant_name":
            extracted_receipt.merchant_name.value = entity.mention_text
            extracted_receipt.merchant_name.confidence = entity.confidence
        elif entity.type == "transaction_date":
            extracted_receipt.receipt_date.value = _parse_date(entity.mention_text)
            extracted_receipt.receipt_date.confidence = entity.confidence
        elif entity.type == "total_amount":
            extracted_receipt.total_amount.value = (
                float(entity.mention_text) if entity.mention_text else None
            )
            extracted_receipt.total_amount.confidence = entity.confidence
            for prop in entity.properties:
                if prop.type == "currency":
                    extracted_receipt.currency.value = prop.mention_text
                    extracted_receipt.currency.confidence = prop.confidence
        elif entity.type == "tax_amount":
            extracted_receipt.tax_amount.value = (
                float(entity.mention_text) if entity.mention_text else None
            )
            extracted_receipt.tax_amount.confidence = entity.confidence
        elif (
            entity.type == "currency"
        ):  # Fallback if currency is not a child of total_amount
            if not extracted_receipt.currency.value:
                extracted_receipt.currency.value = entity.mention_text
                extracted_receipt.currency.confidence = entity.confidence
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
            extracted_receipt.line_items.append(line_item)

    return extracted_receipt
