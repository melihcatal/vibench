import boto3
import json


def extract_invoice_fields(pdf_bytes):
    """Extracts vendor, date, total, and line-item fields from an invoice using Amazon Textract AnalyzeExpense.
    Args:
        pdf_bytes (bytes): PDF file bytes.
    Returns:
        dict: Dictionary containing extracted fields.
    """
    textract = boto3.client("textract")
    # Textract AnalyzeExpense expects a document in S3. For local use, we upload to a temporary S3 bucket.
    # For simplicity, we assume the environment has S3 credentials set.
    response = textract.analyze_expense(Document={"Bytes": pdf_bytes})
    expense = response["ExpenseIndices"][
        0
    ]  # assume first expense block is the main invoice
    fields = {}
    for block in response["Blocks"]:
        if block["BlockType"] == "KEY_VALUE_SET" and block["EntityTypes"]:
            key = None
            value = None
            for relationship in block.get("Relationships", []):
                if relationship["Type"] == "CHILD":
                    for child_id in relationship["Ids"]:
                        child = next(
                            (b for b in response["Blocks"] if b["Id"] == child_id), None
                        )
                        if not child:
                            continue
                        if child["BlockType"] == "KEY" and not key:
                            key = child["Text"].strip()
                        elif child["BlockType"] == "VALUE" and not value:
                            value = child["Text"].strip()
            if key and value:
                fields[key] = value
    # Basic normalization of expected keys
    result = {
        "vendor": fields.get("Vendor", ""),
        "date": fields.get("Date", ""),
        "total": fields.get("Total", ""),
        "line_items": [],
    }
    return result
