# Placeholder – structured field extraction from OCR-normalized text
from typing import Dict, List


def extract_fields(ocr_text: str) -> Dict:
    # Example using Amazon Textract AnalyzeExpense (service=Amazon Textract AnalyzeExpense; sdk=boto3; interface=sdk; auth=AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    # In production you would call boto3 client 'analyze_expense' and parse the response
    # Below is a mock implementation that extracts a few common fields
    fields = {
        "total_amount": None,
        "vendor_name": None,
        "invoice_date": None,
        "due_date": None,
        "line_items": [],
    }
    # --- Mock parsing logic (replace with real client call) ---
    lines = ocr_text.split("\n")
    for line in lines:
        if "Total" in line:
            fields["total_amount"] = line.split(":")[-1].strip()
        elif "Vendor" in line:
            fields["vendor_name"] = line.split(":")[-1].strip()
        elif "Date" in line:
            parts = line.split(":")
            if "Invoice" in parts[0]:
                fields["invoice_date"] = parts[1].strip()
            elif "Due" in parts[0]:
                fields["due_date"] = parts[1].strip()
        # Simple line-item detection (very naive)
        if "Item" in line:
            # capture a dummy line item
            fields["line_items"].append({"description": line, "amount": "0.0"})
    # ------------------------------------------------------------
    return fields
