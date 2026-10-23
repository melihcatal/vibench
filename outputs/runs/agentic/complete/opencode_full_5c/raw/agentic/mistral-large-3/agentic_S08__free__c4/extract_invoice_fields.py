from typing import Dict, Any
from document_client import DocumentClient
from document_models import InvoiceFields, LineItem


def extract_invoice_fields(file_path: str) -> InvoiceFields:
    client = DocumentClient()
    document = client.process_document(file_path)

    vendor = None
    date = None
    total = None
    line_items = []
    confidence = document.confidence

    for entity in document.entities:
        if entity.type_ == "supplier_name":
            vendor = entity.mention_text
        elif entity.type_ == "invoice_date":
            date = entity.mention_text
        elif entity.type_ == "total_amount":
            total = float(entity.mention_text)
        elif entity.type_ == "line_item":
            line_item = LineItem()
            for prop in entity.properties:
                if prop.type_ == "description":
                    line_item.description = prop.mention_text
                elif prop.type_ == "quantity":
                    line_item.quantity = float(prop.mention_text)
                elif prop.type_ == "unit_price":
                    line_item.unit_price = float(prop.mention_text)
                elif prop.type_ == "amount":
                    line_item.amount = float(prop.mention_text)
            line_items.append(line_item)

    return InvoiceFields(
        vendor=vendor,
        date=date,
        total=total,
        line_items=line_items,
        confidence=confidence,
    )
