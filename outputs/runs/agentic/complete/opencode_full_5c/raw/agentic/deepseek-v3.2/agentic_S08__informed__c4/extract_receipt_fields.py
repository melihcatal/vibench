import os
from mindee import Client, product
from mindee.documents import ReceiptV4
from typing import Dict, Any, List


def extract_receipt_fields(image_path: str) -> Dict[str, Any]:
    api_key = os.getenv("MINDEE_API_KEY")

    if not api_key:
        raise ValueError("Mindee API key not configured")

    mindee_client = Client(api_key=api_key)

    with open(image_path, "rb") as f:
        input_doc = mindee_client.source_from_file(f)
        result = mindee_client.parse(ReceiptV4, input_doc)

    receipt = result.document

    merchant = receipt.merchant_name.value if receipt.merchant_name else None
    tax = receipt.tax.value if receipt.tax else None
    total = receipt.total_amount.value if receipt.total_amount else None

    items = []
    if receipt.line_items:
        for line_item in receipt.line_items:
            item_dict = {
                "description": line_item.description.value
                if line_item.description
                else None,
                "quantity": line_item.quantity.value if line_item.quantity else None,
                "unit_price": line_item.unit_price.value
                if line_item.unit_price
                else None,
                "total_amount": line_item.total_amount.value
                if line_item.total_amount
                else None,
            }
            items.append(item_dict)

    confidence = (
        receipt.inference.confidence
        if hasattr(receipt.inference, "confidence")
        else None
    )

    return {
        "merchant": merchant,
        "tax": tax,
        "total": total,
        "items": items,
        "confidence": confidence,
    }
