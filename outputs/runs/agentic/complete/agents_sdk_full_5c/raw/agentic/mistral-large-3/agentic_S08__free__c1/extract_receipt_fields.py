import os
from typing import Dict, Any
import boto3
from document_client import get_textract_client
from document_models import ReceiptExtractionResponse


def extract_receipt_fields(file_path: str) -> ReceiptExtractionResponse:
    client = get_textract_client()

    with open(file_path, "rb") as file:
        content = file.read()

    response = client.analyze_expense(
        Document={"Bytes": content}
    )

    expense_documents = response.get("ExpenseDocuments", [])
    fields = {
        "merchant": "",
        "tax": "",
        "total": "",
        "items": [],
    }

    if expense_documents:
        summary_fields = expense_documents[0].get("SummaryFields", [])
        for field in summary_fields:
            if field.get("Type", {}).get("Text") == "VENDOR_NAME":
                fields["merchant"] = field.get("ValueDetection", {}).get("Text", "")
            elif field.get("Type", {}).get("Text") == "TOTAL":
                fields["total"] = field.get("ValueDetection", {}).get("Text", "")
            elif field.get("Type", {}).get("Text") == "TAX":
                fields["tax"] = field.get("ValueDetection", {}).get("Text", "")

        line_items = expense_documents[0].get("LineItemGroups", [])[0].get("LineItems", []) if expense_documents[0].get("LineItemGroups") else []
        for item in line_items:
            fields["items"].append({
                "description": item.get("LineItemExpenseFields", [])[0].get("ValueDetection", {}).get("Text", ""),
                "amount": item.get("LineItemExpenseFields", [])[1].get("ValueDetection", {}).get("Text", ""),
            })

    return ReceiptExtractionResponse(**fields)