# [SAME-SCENARIO] extract_receipt_fields.py
# Extract merchant, tax, total, and items from a receipt using Amazon Textract
import boto3


def extract_receipt_fields(image_bytes: bytes) -> dict:
    """Extract structured fields from a receipt image.

    Returns a dict with keys: merchant, tax, total, items.
    Uses Amazon Textract (requires AWS credentials/region configured).
    """
    textract = boto3.client("textract")
    # Call AnalyzeExpense (not AnalyzeDocument) which is tuned for receipts
    response = textract.analyze_expense(Document={"Bytes": image_bytes})
    # Simple aggregation logic (replace with actual field paths)
    vendor = None
    tax = None
    total = None
    items = []
    for expense in response["ExpenseFields"]:
        label = expense["LabelDetection"]
        value = expense["ValueDetection"]
        if label == "VENDOR":
            vendor = value["Text"]
        elif label == "TAX":
            tax = value["Text"]
        elif label == "TOTAL":
            total = value["Text"]
        elif label == "LINE_ITEM":
            items.append(value["Text"])
    return {
        "merchant": vendor,
        "tax": tax,
        "total": total,
        "items": items,
    }
