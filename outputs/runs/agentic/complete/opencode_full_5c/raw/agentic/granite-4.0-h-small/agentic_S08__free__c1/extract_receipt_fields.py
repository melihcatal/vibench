# [SAME-SCENARIO] extract_receipt_fields.py

# Uses AWS Textract for receipt field extraction
import boto3
from document_client import DocumentClient


def extract_receipt_fields(image_bytes):
    """Extract merchant, tax, total, and items from a receipt image using AWS Textract.

    Returns a dict with keys: merchant, tax, total, items.
    """
    textract = boto3.client("textract")
    response = textract.analyze_document(
        Document={"Bytes": image_bytes}, FeatureTypes=["FORMS"]
    )
    fields = {"merchant": "", "tax": "", "total": "", "items": []}
    for block in response["Blocks"]:
        if block["BlockType"] == "KEY_VALUE_SET":
            key = next(
                (item for item in block["Entities"] if item["Type"] == "KEY"), None
            )
            if key and key["Text"].lower() == "merchant":
                val = next(
                    (item for item in block["Entities"] if item["Type"] == "VALUE"),
                    None,
                )
                fields["merchant"] = val["Text"] if val else ""
            elif key and key["Text"].lower() == "tax":
                val = next(
                    (item for item in block["Entities"] if item["Type"] == "VALUE"),
                    None,
                )
                fields["tax"] = val["Text"] if val else ""
            elif key and key["Text"].lower() == "total":
                val = next(
                    (item for item in block["Entities"] if item["Type"] == "VALUE"),
                    None,
                )
                fields["total"] = val["Text"] if val else ""
        elif block["BlockType"] == "LINE":
            text = block["Text"].strip()
            # simple heuristic: any non-empty line is an item
            if text:
                fields["items"].append(text)
    return fields
