from typing import Dict, Any, List
from document_client import DocumentClient
from document_models import ReceiptFields


def extract_receipt_fields(file_path: str) -> ReceiptFields:
    client = DocumentClient()
    document = client.process_document(file_path)

    merchant = None
    tax = None
    total = None
    items = []
    confidence = document.confidence

    for entity in document.entities:
        if entity.type_ == "merchant_name":
            merchant = entity.mention_text
        elif entity.type_ == "total_tax":
            tax = float(entity.mention_text)
        elif entity.type_ == "total_amount":
            total = float(entity.mention_text)
        elif entity.type_ == "line_item":
            item = {
                "description": None,
                "quantity": None,
                "price": None,
            }
            for prop in entity.properties:
                if prop.type_ == "description":
                    item["description"] = prop.mention_text
                elif prop.type_ == "quantity":
                    item["quantity"] = float(prop.mention_text)
                elif prop.type_ == "price":
                    item["price"] = float(prop.mention_text)
            items.append(item)

    return ReceiptFields(
        merchant=merchant,
        tax=tax,
        total=total,
        items=items,
        confidence=confidence,
    )
