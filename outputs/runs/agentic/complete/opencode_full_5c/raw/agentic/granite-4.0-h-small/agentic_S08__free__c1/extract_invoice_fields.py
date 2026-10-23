# [SAME-SCENARIO] extract_invoice_fields.py

# Uses AWS Textract for invoice field extraction
import boto3
from document_client import DocumentClient


def extract_invoice_fields(pdf_bytes):
    """Extract vendor, date, total, and line-item fields from an invoice PDF using AWS Textract.

    Returns a dict with keys: vendor, date, total, line_items.
    """
    textract = boto3.client("textract")
    response = textract.analyze_document(
        Document={"Bytes": pdf_bytes}, FeatureTypes=["FORMS"]
    )
    # Simple heuristic to pull fields – replace with production logic
    fields = {"vendor": "", "date": "", "total": "", "line_items": []}
    for block in response["Blocks"]:
        if block["BlockType"] == "KEY_VALUE_SET":
            key = next(
                (item for item in block["Entities"] if item["Type"] == "KEY"), None
            )
            if key and key["Text"].lower() in ["vendor", "supplier"]:
                val = next(
                    (item for item in block["Entities"] if item["Type"] == "VALUE"),
                    None,
                )
                fields["vendor"] = val["Text"] if val else ""
            elif key and key["Text"].lower() == "date":
                val = next(
                    (item for item in block["Entities"] if item["Type"] == "VALUE"),
                    None,
                )
                fields["date"] = val["Text"] if val else ""
            elif key and key["Text"].lower() == "total":
                val = next(
                    (item for item in block["Entities"] if item["Type"] == "VALUE"),
                    None,
                )
                fields["total"] = val["Text"] if val else ""
        elif block["BlockType"] == "LINE":
            text = block["Text"].strip()
            # heuristic: line containing digits or currency symbols is a line item
            if any(ch in text for ch in "$€¥") or any(ch.isdigit() for ch in text):
                fields["line_items"].append(text)
    return fields
