import os
import boto3
from document_models import RawReceipt


def extract_receipt_fields(document_path: str) -> RawReceipt:
    textract = boto3.client(
        "textract", region_name=os.getenv("AWS_REGION", "us-east-1")
    )

    with open(document_path, "rb") as file:
        img_bytes = file.read()

    response = textract.analyze_expense_document(
        Document={"Bytes": img_bytes}, FeatureTypes=["EXPENSES"]
    )

    expense_doc = response["ExpenseDocuments"][0]
    summary = expense_doc["SummaryPages"][0].get("ReceiptSummary", {})

    merchant = summary.get("VendorName", {}).get("Text", "")
    tax = float(summary.get("TaxTotals", [{}])[0].get("Total", {}).get("Text", 0) or 0)
    total = float(summary.get("TransactionTotal", {}).get("Text", 0) or 0)

    items = []
    line_groups = summary.get("LineItemGroups", [])
    for group in line_groups:
        for item in group.get("LineItems", []):
            items.append(item.get("Description", {}).get("Text", ""))

    return RawReceipt(merchant=merchant, tax=tax, total=total, items=items)
