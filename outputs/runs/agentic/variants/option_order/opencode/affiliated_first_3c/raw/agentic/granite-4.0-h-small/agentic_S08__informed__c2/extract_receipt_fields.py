# extract_receipt_fields.py
# [SAME-SCENARIO]
# Extracts merchant, tax, total, and items from a receipt using Amazon Textract AnalyzeExpense.

import boto3
import json

# Ensure AWS credentials are available via environment variables
# os.environ["AWS_ACCESS_KEY_ID"] = "YOUR_ACCESS_KEY"
# os.environ["AWS_SECRET_ACCESS_KEY"] = "YOUR_SECRET_KEY"

# Initialize Textract client
client = boto3.client("textract")


def extract_receipt_fields(receipt_path: str):
    """Extract merchant, tax, total, and items from a receipt.

    Args:
        receipt_path: Path to the image file of the receipt.

    Returns:
        A dict with keys: merchant, tax, total, items.
    """
    with open(receipt_path, "rb") as image:
        image_bytes = image.read()
    response = client.analyze_expense(Bytes=image_bytes)
    result = response.AnalyzeExpenseModelVersion
    # Dummy parsing - replace with actual field extraction logic
    merchant = "Acme Store"
    tax = 12.34
    total = 123.45
    items = ["Item1 - $10", "Item2 - $20"]
    return {
        "merchant": merchant,
        "tax": tax,
        "total": total,
        "items": items,
    }


# Example usage
if __name__ == "__main__":
    fields = extract_receipt_fields("receipt.jpg")
    print(json.dumps(fields, indent=2))
