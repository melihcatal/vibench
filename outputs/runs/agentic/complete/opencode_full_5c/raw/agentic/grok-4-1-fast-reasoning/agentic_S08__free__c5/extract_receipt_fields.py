import os
import boto3
from document_models import ReceiptFields
from typing import Dict, Any, List


def extract_receipt_fields(document_bytes: bytes) -> ReceiptFields:
    textract = boto3.client(
        "textract", region_name=os.getenv("AWS_REGION", "us-east-1")
    )
    response = textract.analyze_document(
        Document={"Bytes": document_bytes}, FeatureTypes=["FORMS"]
    )
    key_map: Dict[str, str] = {}
    for block in response["Blocks"]:
        if block["BlockType"] == "KEY_VALUE_SET":
            if (
                "EntityTypes" in block
                and block["EntityTypes"]
                and block["EntityTypes"][0] == "KEY"
            ):
                key_map[block["Text"].lower()] = ""
    merchant = key_map.get("merchant", "")
    tax_str = key_map.get("tax", "0").replace("$", "")
    tax = float(tax_str) if tax_str else 0.0
    total_str = key_map.get("total", "0").replace("$", "")
    total = float(total_str) if total_str else 0.0
    items: List[Dict[str, Any]] = []
    return {"merchant": merchant, "tax": tax, "total": total, "items": items}
