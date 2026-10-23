import boto3
from typing import List, Dict, Any

from document_client import get_aws_credentials
from document_models import ParsedReceipt

def extract_receipt_fields(bucket: str, document: str) -> ParsedReceipt:
    """
    Extracts fields from a receipt using Amazon Textract.
    """
    aws_creds = get_aws_credentials()
    session = boto3.Session(
        aws_access_key_id=aws_creds["access_key_id"],
        aws_secret_access_key=aws_creds["secret_access_key"],
        region_name=aws_creds["region"],
    )
    client = session.client("textract")

    response = client.analyze_expense(
        Document={'S3Object': {'Bucket': bucket, 'Name': document}}
    )

    merchant_name = ""
    tax = ""
    total = ""
    items = []

    for expense_doc in response.get("ExpenseDocuments", []):
        for field in expense_doc.get("SummaryFields", []):
            field_type = field.get("Type", {}).get("Text")
            field_value = field.get("ValueDetection", {}).get("Text")

            if field_type == "VENDOR_NAME":
                merchant_name = field_value
            elif field_type == "TOTAL":
                total = field_value
            elif field_type == "TAX":
                tax = field_value

        for line_item_group in expense_doc.get("LineItemGroups", []):
            for line_item in line_item_group.get("LineItems", []):
                item = {}
                for field in line_item.get("LineItemExpenseFields", []):
                    field_type = field.get("Type", {}).get("Text")
                    field_value = field.get("ValueDetection", {}).get("Text")
                    if field_type == "ITEM":
                        item['description'] = field_value
                    elif field_type == "PRICE":
                        item['price'] = field_value
                if item.get('description'):
                    items.append(item)


    return ParsedReceipt(
        merchant=merchant_name,
        tax=tax,
        total=total,
        items=items,
    )
