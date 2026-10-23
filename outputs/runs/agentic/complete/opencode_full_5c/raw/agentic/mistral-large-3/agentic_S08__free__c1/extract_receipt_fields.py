from typing import Dict, Any
from document_client import DocumentClient
from document_models import ReceiptFields, parse_date


def extract_receipt_fields(file_path: str) -> Dict[str, Any]:
    client = DocumentClient()
    document = client.process_document(file_path)

    receipt_data = {
        "merchant": None,
        "tax": None,
        "total": None,
        "items": [],
        "confidence": document.confidence,
    }

    for entity in document.entities:
        if entity.type_ == "merchant_name":
            receipt_data["merchant"] = entity.mention_text
        elif entity.type_ == "total_tax":
            receipt_data["tax"] = float(entity.mention_text)
        elif entity.type_ == "total_amount":
            receipt_data["total"] = float(entity.mention_text)
        elif entity.type_ == "line_item":
            item = {}
            for prop in entity.properties:
                if prop.type_ == "description":
                    item["description"] = prop.mention_text
                elif prop.type_ == "price":
                    item["price"] = (
                        float(prop.mention_text) if prop.mention_text else None
                    )
                elif prop.type_ == "quantity":
                    item["quantity"] = (
                        float(prop.mention_text) if prop.mention_text else None
                    )
            if item:
                receipt_data["items"].append(item)

    return ReceiptFields(**receipt_data).dict()
