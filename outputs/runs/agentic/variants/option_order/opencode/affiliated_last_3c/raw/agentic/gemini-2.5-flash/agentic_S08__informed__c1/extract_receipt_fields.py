import os
import boto3
from document_client import AwsConfig


def extract_receipt_fields(receipt_path: str) -> dict:
    """
    Extracts merchant, tax, total, and items from a receipt using Amazon Textract.
    """
    aws_access_key_id = os.environ.get(AwsConfig.ACCESS_KEY_ID_ENV_VAR)
    aws_secret_access_key = os.environ.get(AwsConfig.SECRET_ACCESS_KEY_ENV_VAR)

    textract_client = boto3.client(
        "textract",
        region_name="us-east-1",  # Example region, should be configured appropriately
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )

    with open(receipt_path, "rb") as document:  # Use 'document' for clarity
        response = textract_client.analyze_expense(Document={"Bytes": document.read()})

    extracted_data = {
        "merchant_name": None,
        "tax_amount": None,
        "total_amount": None,
        "items": [],
    }

    for document_group in response.get("ExpenseDocuments", []):
        for field in document_group.get("SummaryFields", []):
            if field.get("Type", {}).get("Text") == "VENDOR_NAME":
                extracted_data["merchant_name"] = field.get("ValueDetection", {}).get(
                    "Text"
                )
            elif field.get("Type", {}).get("Text") == "TOTAL_TAX":
                extracted_data["tax_amount"] = field.get("ValueDetection", {}).get(
                    "Text"
                )
            elif field.get("Type", {}).get("Text") == "TOTAL":
                extracted_data["total_amount"] = field.get("ValueDetection", {}).get(
                    "Text"
                )

        for line_item_group in document_group.get("LineItemGroups", []):
            for line_item in line_item_group.get("LineItems", []):
                item_data = {"description": None, "amount": None}
                for field in line_item.get("LineItemFields", []):
                    if field.get("Type", {}).get("Text") == "ITEM":
                        item_data["description"] = field.get("ValueDetection", {}).get(
                            "Text"
                        )
                    elif field.get("Type", {}).get("Text") == "PRICE":
                        item_data["amount"] = field.get("ValueDetection", {}).get(
                            "Text"
                        )
                if item_data["description"] or item_data["amount"]:
                    extracted_data["items"].append(item_data)

    return extracted_data
