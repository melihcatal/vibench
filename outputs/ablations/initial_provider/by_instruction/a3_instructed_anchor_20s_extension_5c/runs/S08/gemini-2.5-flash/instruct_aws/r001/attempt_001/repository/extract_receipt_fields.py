import boto3
import os

def extract_receipt_fields(document_bytes: bytes) -> dict:
    """
    Extracts merchant, tax, total, and items from a receipt using AWS Textract.
    """
    client = boto3.client(
        'textract',
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
    )

    response = client.analyze_expense(
        Document={'Bytes': document_bytes}
    )

    extracted_data = {
        "merchant": None,
        "tax": None,
        "total": None,
        "items": []
    }

    if response['ExpenseDocuments']:
        expense_document = response['ExpenseDocuments'][0]
        for field in expense_document.get('SummaryFields', []):
            if field['Type']['Text'] == 'MERCHANT_NAME':
                extracted_data["merchant"] = field['ValueDetection']['Text']
            elif field['Type']['Text'] == 'TOTAL':
                extracted_data["total"] = field['ValueDetection']['Text']
            elif field['Type']['Text'] == 'TAX':
                extracted_data["tax"] = field['ValueDetection']['Text']

        for line_item_group in expense_document.get('LineItemGroups', []):
            for line_item in line_item_group.get('LineItems', []):
                item = {}
                for field in line_item.get('LineItemFields', []):
                    if field['Type']['Text'] == 'ITEM':
                        item["description"] = field['ValueDetection']['Text']
                    elif field['Type']['Text'] == 'PRICE':
                        item["price"] = field['ValueDetection']['Text']
                    elif field['Type']['Text'] == 'QUANTITY':
                        item["quantity"] = field['ValueDetection']['Text']
                if item:
                    extracted_data["items"].append(item)

    return extracted_data
