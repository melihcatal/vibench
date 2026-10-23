import os
from typing import Dict, List, Any
import json
import boto3
from botocore.exceptions import ClientError


def extract_receipt_fields(receipt_path: str) -> Dict[str, Any]:
    """
    Extract merchant, tax, total, and items from a receipt using AWS Textract.
    """
    textract_client = boto3.client(
        "textract",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )

    with open(receipt_path, "rb") as f:
        image_bytes = f.read()

    response = textract_client.analyze_expense(Document={"Bytes": image_bytes})

    extracted_data = {"merchant": None, "tax": None, "total": None, "items": []}

    for expense_doc in response.get("ExpenseDocuments", []):
        for summary_field in expense_doc.get("SummaryFields", []):
            field_type = summary_field.get("Type", {}).get("Text", "").lower()
            field_text = summary_field.get("ValueDetection", {}).get("Text", "")

            if field_type == "vendor" or field_type == "merchant":
                extracted_data["merchant"] = field_text
            elif field_type == "total":
                try:
                    extracted_data["total"] = float(
                        field_text.replace("$", "").replace(",", "")
                    )
                except (ValueError, AttributeError):
                    extracted_data["total"] = field_text
            elif field_type == "tax":
                try:
                    extracted_data["tax"] = float(
                        field_text.replace("$", "").replace(",", "")
                    )
                except (ValueError, AttributeError):
                    extracted_data["tax"] = field_text

        for line_item_group in expense_doc.get("LineItemGroups", []):
            for line_item in line_item_group.get("LineItems", []):
                item_data = {}
                for expense_field in line_item.get("LineItemExpenseFields", []):
                    field_type = expense_field.get("Type", {}).get("Text", "").lower()
                    field_text = expense_field.get("ValueDetection", {}).get("Text", "")

                    if field_type == "item":
                        item_data["description"] = field_text
                    elif field_type == "price":
                        try:
                            item_data["price"] = float(
                                field_text.replace("$", "").replace(",", "")
                            )
                        except (ValueError, AttributeError):
                            item_data["price"] = field_text
                    elif field_type == "quantity":
                        try:
                            item_data["quantity"] = float(field_text)
                        except (ValueError, AttributeError):
                            item_data["quantity"] = field_text

                if item_data:
                    extracted_data["items"].append(item_data)

    return extracted_data
