import os
from mindee import MindeeClient
from mindee.product.receipt import Receipt
from document_client import load_image


def extract_receipt_fields(image_path: str) -> dict:
    api_key = os.getenv("MINDEE_API_KEY")
    if not api_key:
        raise ValueError("MINDEE_API_KEY env var required")

    client = MindeeClient(api_key=api_key)
    document = client.load_document(Receipt, load_image(image_path))
    result = document.parse()

    prediction = result.document.inference.prediction
    fields_dict = {}
    fields_dict["merchant"] = prediction.supplier or ""
    fields_dict["date"] = prediction.date.value if prediction.date else ""
    fields_dict["tax"] = prediction.taxes.total_amount if prediction.taxes else None
    fields_dict["total"] = prediction.total_including_tax or 0.0

    items = []
    for p in prediction.products or []:
        item = {
            "description": p.description or "",
            "quantity": getattr(p, "quantity", None),
            "unit_price": getattr(p, "unit_price", None),
            "amount": p.total_amount or 0.0,
        }
        items.append(item)
    fields_dict["items"] = items

    fields_dict["confidence"] = {"overall": result.document.confidence}

    return fields_dict
