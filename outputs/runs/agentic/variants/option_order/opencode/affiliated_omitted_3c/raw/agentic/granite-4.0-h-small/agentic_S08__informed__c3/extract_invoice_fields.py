import boto3
import os

# Amazon Textract AnalyzeExpense
client = boto3.client("textract")


def extract_invoice_fields(file_bytes):
    # Call Textract AnalyzeExpense API
    response = client.analyze_expense(Document={"Bytes": file_bytes})
    # Extract vendor, date, total, line items
    invoice = {}
    for block in response["ExpenseDocuments"][0]["ExpenseFields"]:
        if block["Type"]["Text"] == "VENDOR":
            invoice["vendor"] = block["ValueDetection"]["Text"]
        elif block["Type"]["Text"] == "DATE":
            invoice["date"] = block["ValueDetection"]["Text"]
        elif block["Type"]["Text"] == "TOTAL":
            invoice["total"] = block["ValueDetection"]["Text"]
        elif block["Type"]["Text"] == "LINE_ITEM":
            if "Vendor" in block:
                vendor = block["Vendor"]
            line_item = {
                "vendor": vendor if "vendor" in locals() else None,
                "description": block["Text"] if "Text" in block else None,
                "amount": block.get("AmountValue", {}).get("Text"),
            }
            invoice.setdefault("line_items", []).append(line_item)
    return invoice
