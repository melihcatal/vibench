import os
from typing import Dict, Any, List
import boto3
from document_client import DocumentClients, AWS_REGION
from document_models import Receipt, LineItem
import datetime

def extract_receipt_fields(document_bytes: bytes, document_id: str = None) -> Receipt:
    """Extracts merchant, tax, total, and items from a receipt using AWS Textract's AnalyzeExpense.

    Args:
        document_bytes: The content of the document as bytes.
        document_id: Optional unique identifier for the document.

    Returns:
        A Receipt dataclass instance.
    """
    client = DocumentClients.get_textract_client()

    response = client.analyze_expense(Document={'Bytes': document_bytes})

    merchant_name = None
    transaction_date = None
    total_amount = None
    tax_amount = None
    currency = None
    items: List[LineItem] = []

    # Iterate through expense documents (usually one per call for a single document)
    for expense_doc in response.get('ExpenseDocuments', []):
        # Extract summary fields
        summary_fields = expense_doc.get('SummaryFields', [])
        for field in summary_fields:
            field_type = field.get('Type', {}).get('Text')
            field_value = field.get('ValueDetection', {}).get('Text')

            if field_type == 'MERCHANT_NAME':
                merchant_name = field_value
            elif field_type == 'DATE' and field_value:
                try:
                    transaction_date = datetime.datetime.strptime(field_value, "%m/%d/%Y").date() # Common receipt date format
                except ValueError:
                    try:
                        transaction_date = datetime.datetime.strptime(field_value, "%Y-%m-%d").date() # Another common format
                    except ValueError:
                        pass
            elif field_type == 'TOTAL' and field_value:
                try:
                    total_amount = float(field_value.replace('$', '').replace(',', ''))
                except ValueError: pass
                currency = field.get('ValueDetection', {}).get('Currency')
            elif field_type == 'TAX' and field_value:
                try:
                    tax_amount = float(field_value.replace('$', '').replace(',', ''))
                except ValueError: pass

        # Extract line items
        line_item_groups = expense_doc.get('LineItemGroups', [])
        for group in line_item_groups:
            for item_detail in group.get('LineItems', []):
                item_description = None
                item_quantity = None
item_unit_price = None
                item_total_amount = None

                for field in item_detail.get('LineItemFields', []):
                    field_type = field.get('Type', {}).get('Text')
                    field_value = field.get('ValueDetection', {}).get('Text')
                    if field_type == 'ITEM_DESCRIPTION':
                        item_description = field_value
                    elif field_type == 'QUANTITY':
                        try: item_quantity = float(field_value)
                        except ValueError: pass
                    elif field_type == 'PRICE': # Textract often gives per-item price here
                        try: item_unit_price = float(field_value.replace('$', '').replace(',', ''))
                        except ValueError: pass
                    elif field_type == 'TOTAL_PRICE': # Or total for the line item
                        try: item_total_amount = float(field_value.replace('$', '').replace(',', ''))
                        except ValueError: pass

                items.append(LineItem(
                    description=item_description,
                    quantity=item_quantity,
                    unit_price=item_unit_price,
                    total_amount=item_total_amount # This might be the raw total, standardization can happen later
                ))

    return Receipt(
        merchant_name=merchant_name,
        transaction_date=transaction_date,
        total_amount=total_amount,
        tax_amount=tax_amount,
        currency=currency,
        items=items,
        raw_document_url="", # In a real scenario, this would be an S3 URL
        document_id=document_id
    )
