import boto3
from document_client import get_aws_textract_client
from document_models import ExtractedReceiptFields, ReceiptItem
from typing import Dict, Any, Optional

def extract_receipt_fields_textract(file_content: bytes) -> ExtractedReceiptFields:
    """
    Extracts receipt fields using AWS Textract's AnalyzeExpense API.
    Requires AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION_NAME environment variables.
    """
    client = get_aws_textract_client()

    response = client.analyze_expense(Document={'Bytes': file_content})

    merchant_name = None
    transaction_date = None
    total_amount = None
    tax_amount = None
    currency = None
    items_data = []
    raw_text = ""

    if response.get('ExpenseDocuments'):
        expense_doc = response['ExpenseDocuments'][0]
        for field in expense_doc.get('SummaryFields', []):
            if field.get('Type', {}).get('Text') == 'VENDOR_NAME':
                merchant_name = field.get('ValueDetection', {}).get('Text')
            elif field.get('Type', {}).get('Text') == 'DATE':
                transaction_date = field.get('ValueDetection', {}).get('Text')
            elif field.get('Type', {}).get('Text') == 'TOTAL':
                total_amount_str = field.get('ValueDetection', {}).get('Text')
                try:
                    total_amount = float(total_amount_str)
                except (ValueError, TypeError):
                    total_amount = None
                currency = field.get('ValueDetection', {}).get('Currency')
            elif field.get('Type', {}).get('Text') == 'TAX':
                tax_amount_str = field.get('ValueDetection', {}).get('Text')
                try:
                    tax_amount = float(tax_amount_str)
                except (ValueError, TypeError):
                    tax_amount = None

        for line_item_group in expense_doc.get('LineItemGroups', []):
            for line_item in line_item_group.get('LineItems', []):
                item = ReceiptItem()
                for field in line_item.get('LineItemFields', []):
                    field_type = field.get('Type', {}).get('Text')
                    field_value = field.get('ValueDetection', {}).get('Text')
                    try:
                        if field_type == 'ITEM':
                            item.description = field_value
                        elif field_type == 'QUANTITY':
                            item.quantity = float(field_value)
                        elif field_type == 'PRICE':
                            item.unit_price = float(field_value)
                        elif field_type == 'TOTAL':
                            item.amount = float(field_value)
                    except (ValueError, TypeError):
                        pass
                if item.description or item.quantity or item.unit_price or item.amount:
                    items_data.append(item)

    return ExtractedReceiptFields(
        merchant_name=merchant_name,
        transaction_date=transaction_date,
        total_amount=total_amount,
        tax_amount=tax_amount,
        currency=currency,
        items=items_data,
        raw_text=raw_text
    )
