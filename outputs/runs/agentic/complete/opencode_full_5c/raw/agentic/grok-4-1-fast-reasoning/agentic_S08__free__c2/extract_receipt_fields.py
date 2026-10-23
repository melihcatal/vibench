import os
import boto3
from document_client import load_document
from typing import Dict, Any
import json


def extract_receipt_fields(image_path: str) -> Dict[str, Any]:
    aws_region = os.getenv("AWS_REGION", "us-east-1")
    textract = boto3.client("textract", region_name=aws_region)

    document_bytes, _ = load_document(image_path)

    response = textract.analyze_expense(Document={"Bytes": document_bytes})

    blocks = response["Blocks"]
    merchant = ""
    tax = None
    total = 0.0
    items = []
    confidence = {}

    for block in blocks:
        if "Confidence" in block:
            confidence[block["Id"]] = block["Confidence"]
        if block["BlockType"] == "MERCHANT_NAME":
            merchant = block["Text"]
        elif block["BlockType"] == "LINE_ITEM_GROUP":
            for rel in block.get("Relationships", []):
                if rel["Type"] == "CHILD":
                    child_id = rel["Ids"][0]
                    child_block = next(b for b in blocks if b["Id"] == child_id)
                    items.append(child_block["Text"])
        elif block["BlockType"] == "SUMMARY_TABLE":
            # Parse summary for tax total
            pass  # Simplified

    return {
        "merchant": merchant,
        "tax": tax,
        "total": total,
        "items": items,
        "confidence": confidence,
    }
