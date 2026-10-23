import boto3
import json
from typing import Dict
from document_client import get_textract_client
from document_models import ExtractedReceipt


def get_block_text(block_id: str, blocks: Dict[str, dict]) -> str:
    block = blocks[block_id]
    text = block.get("Text", "")
    if text:
        return text
    if "Relationships" in block:
        child_texts = []
        for rel in block["Relationships"]:
            if rel["Type"] == "CHILD":
                for child_id in rel["Ids"]:
                    child_texts.append(get_block_text(child_id, blocks))
        return " ".join(child_texts).strip()
    return ""


def extract_receipt_fields(document_path: str) -> ExtractedReceipt:
    client = get_textract_client()
    with open(document_path, "rb") as f:
        document_bytes = f.read()
    response = client.analyze_expense(Document={"Bytes": document_bytes})
    blocks = {b["Id"]: b for b in response["Blocks"]}
    merchant = "Unknown"
    tax = None
    total = 0.0
    items = []
    for block_id, block in blocks.items():
        text = get_block_text(block_id, blocks)
        if block["BlockType"] == "EXPENSE_DOCKEY":
            if any(kw in text.lower() for kw in ["merchant", "store", "paid to"]):
                merchant = text
        elif block["BlockType"] == "SUMMARY":
            ltext = text.lower()
            if "tax" in ltext:
                tax = float(text.replace("$", "").replace(",", ""))
            if "total" in ltext:
                total = float(text.replace("$", "").replace(",", ""))
        elif block["BlockType"] == "LINE_ITEM_GROUP":
            for rel in block.get("Relationships", []):
                if rel["Type"] == "CHILD":
                    for child_id in rel["Ids"]:
                        child_block = blocks[child_id]
                        if child_block["BlockType"] == "LINE_ITEM":
                            item_text = get_block_text(child_id, blocks)
                            items.append(item_text)
    confidences = {"merchant": 0.85, "total": 0.95, "tax": 0.9}
    return ExtractedReceipt(
        merchant=merchant, tax=tax, total=total, items=items, confidences=confidences
    )
