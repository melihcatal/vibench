import os
import boto3

# Provider: Amazon Textract AnalyzeExpense


def extract_receipt_fields(jpg_bytes):
    """Extract merchant, tax, total, and items from a receipt (JPG bytes)."""
    textract = boto3.client(
        "textract",
        region_name=os.getenv("AWS_REGION"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
    # Call AnalyzeExpense API (works for receipts as well)
    response = textract.analyze_document(
        Document={"Bytes": jpg_bytes}, FeatureTypes=["Expense"]
    )
    receipt = {}
    for block in response["Blocks"]:
        block_type = block["BlockType"]
        if block_type == "KEY_VALUE_SET":
            if block["EntityTypes"][0] == "MERCHANT":
                receipt["merchant"] = block["Text"]
        elif block_type == "LINE":
            # Simple heuristic: treat each line as an item
            receipt.setdefault("items", []).append(block["Text"])
    # Extract tax and total from KEY_VALUE_SET if present
    for block in response["Blocks"]:
        if block["BlockType"] == "KEY_VALUE_SET":
            key = block.get("EntityTypes")
            if not key:
                continue
            key = key[0]
            value = block["Text"]
            if key == "SUBTOTAL":
                receipt["subtotal"] = value
            elif key == "TAX":
                receipt["tax"] = value
            elif key == "TOTAL":
                receipt["total"] = value
    return receipt
