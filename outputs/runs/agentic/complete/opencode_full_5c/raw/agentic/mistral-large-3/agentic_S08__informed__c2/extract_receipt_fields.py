import boto3
import os
from typing import Dict, Any, List
from datetime import datetime

# Provider-specific: Amazon Textract AnalyzeExpense
textract = boto3.client(
    "textract",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION", "us-east-1"),
)


def extract_receipt_fields(file_path: str) -> Dict[str, Any]:
    """
    Extracts merchant, tax, total, and items from a receipt using Amazon Textract AnalyzeExpense.
    """
    with open(file_path, "rb") as file:
        document_bytes = file.read()

    response = textract.analyze_expense(Document={"Bytes": document_bytes})

    merchant = ""
    tax = 0.0
    total = 0.0
    items = []

    for expense_doc in response.get("ExpenseDocuments", []):
        for summary_field in expense_doc.get("SummaryFields", []):
            if summary_field.get("Type", {}).get("Text") == "VENDOR_NAME":
                merchant = summary_field.get("ValueDetection", {}).get("Text", "")
            elif summary_field.get("Type", {}).get("Text") == "TOTAL":
                total = float(summary_field.get("ValueDetection", {}).get("Text", "0"))
            elif summary_field.get("Type", {}).get("Text") == "TAX":
                tax = float(summary_field.get("ValueDetection", {}).get("Text", "0"))

        for line_item_group in expense_doc.get("LineItemGroups", []):
            for line_item in line_item_group.get("LineItems", []):
                item = {}
                for field in line_item.get("LineItemExpenseFields", []):
                    if field.get("Type", {}).get("Text") == "ITEM":
                        item["description"] = field.get("ValueDetection", {}).get(
                            "Text", ""
                        )
                    elif field.get("Type", {}).get("Text") == "PRICE":
                        item["amount"] = float(
                            field.get("ValueDetection", {}).get("Text", "0")
                        )
                    elif field.get("Type", {}).get("Text") == "QUANTITY":
                        item["quantity"] = float(
                            field.get("ValueDetection", {}).get("Text", "1")
                        )
                items.append(item)

    return {
        "merchant": merchant,
        "tax": tax,
        "total": total,
        "items": items,
        "confidence": 0.9,  # Textract does not provide confidence for AnalyzeExpense
        "provider": "amazon_textract",
    }
