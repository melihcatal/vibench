import boto3
import os

# AWS Textract (general document OCR) as same‑scenario fallback for receipts
client = boto3.client("textract")


def extract_receipt_fields(file_bytes):
    # Textract does not have a dedicated receipt model, so we use the generic
    # AnalyzeDocument call with FEATURE_FLAGS set for OCR
    response = client.analyze_document(
        Document={"Bytes": file_bytes}, FeatureFlags=["FORMS", "TABLES"]
    )
    receipt = {}
    # Gather merchant name (often in headers)
    for block in response["Blocks"]:
        if block["BlockType"] == "KEY_VALUE_SET":
            if block["EntityTypes"] and "MERCHANT" in block["EntityTypes"]:
                receipt["merchant"] = block["Text"]
        elif block["BlockType"] == "LINE":
            if "TEXT" in block:
                # Approximate heuristics for tax, total and items
                text = block["Text"].upper()
                if "TOTAL" in text:
                    receipt["total"] = block["Text"]
                elif "TAX" in text:
                    receipt["tax"] = block["Text"]
                else:
                    # Store each line as an item
                    receipt.setdefault("items", []).append(block["Text"])
    return receipt
