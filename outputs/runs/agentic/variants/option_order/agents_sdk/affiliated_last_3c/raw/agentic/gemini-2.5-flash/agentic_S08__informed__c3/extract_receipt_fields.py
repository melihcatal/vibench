import os
from mindee import Client, product

def extract_receipt_fields(api_key: str, file_path: str) -> dict:
    """
    Extracts merchant, tax, total, and items from a receipt using Mindee.
    """
    mindee_client = Client(api_key=api_key)
    input_doc = mindee_client.doc_from_path(file_path)

    receipt_parser = mindee_client.parse(input_doc, product.ReceiptV5)

    extracted_data = {
        "merchant_name": None,
        "total_tax": None,
        "total_amount": None,
        "line_items": []
    }

    if receipt_parser.document.inference.prediction.locale.value:
        extracted_data["currency"] = receipt_parser.document.inference.prediction.locale.currency

    if receipt_parser.document.inference.prediction.supplier_name.value:
        extracted_data["merchant_name"] = receipt_parser.document.inference.prediction.supplier_name.value

    if receipt_parser.document.inference.prediction.total_tax.value:
        extracted_data["total_tax"] = receipt_parser.document.inference.prediction.total_tax.value

    if receipt_parser.document.inference.prediction.total_amount.value:
        extracted_data["total_amount"] = receipt_parser.document.inference.prediction.total_amount.value

    for item in receipt_parser.document.inference.prediction.line_items:
        extracted_data["line_items"].append({
            "description": item.description,
            "quantity": item.qty,
            "unit_price": item.unit_price,
            "total_price": item.total_amount,
        })
    return extracted_data
