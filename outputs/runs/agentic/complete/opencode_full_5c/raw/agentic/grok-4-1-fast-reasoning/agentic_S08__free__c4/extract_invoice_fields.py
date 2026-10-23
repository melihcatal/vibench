import boto3
import json
from typing import Dict
from document_client import get_textract_client
from document_models import ExtractedInvoice, LineItem


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


def extract_invoice_fields(document_path: str) -> ExtractedInvoice:
    client = get_textract_client()
    with open(document_path, "rb") as f:
        document_bytes = f.read()
    response = client.analyze_expense(Document={"Bytes": document_bytes})
    blocks = {b["Id"]: b for b in response["Blocks"]}
    vendor = "Unknown"
    invoice_date = "Unknown"
    total = 0.0
    line_items = []
    for block_id, block in blocks.items():
        text = get_block_text(block_id, blocks)
        if block["BlockType"] == "EXPENSE_DOCKEY":
            if any(kw in text.lower() for kw in ["vendor", "bill from", "sold to"]):
                vendor = text
            if "date" in text.lower():
                invoice_date = text
        elif block["BlockType"] == "SUMMARY":
            if "total" in text.lower():
                total = float(text.replace("$", "").replace(",", ""))
        elif block["BlockType"] == "LINE_ITEM_GROUP":
            for rel in block.get("Relationships", []):
                if rel["Type"] == "CHILD":
                    for child_id in rel["Ids"]:
                        child_block = blocks[child_id]
                        if child_block["BlockType"] == "LINE_ITEM":
                            desc = ""
                            qty = None
                            unit_price = None
                            amount = 0.0
                            ctext = get_block_text(child_id, blocks)
                            # Simple parse from text
                            words = ctext.split()
                            if len(words) >= 4:
                                desc = " ".join(words[:-3])
                                amount = float(words[-1].replace("$", ""))
                            line_items.append(LineItem(description=desc, amount=amount))
    confidences = {"vendor": 0.85, "invoice_date": 0.9, "total": 0.95}
    return ExtractedInvoice(
        vendor=vendor,
        invoice_date=invoice_date,
        total=total,
        line_items=line_items,
        confidences=confidences,
    )
