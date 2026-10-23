import os
from typing import Dict, Any, List, Optional
import boto3
from document_models import DocumentExtractionResult, LineItem

def extract_receipt_fields(image_content: bytes) -> DocumentExtractionResult:
    client = boto3.client('textract', region_name=os.environ.get("AWS_REGION"))

    response = client.analyze_expense(Document={'Bytes': image_content})

    merchant_name: Optional[str] = None
    tax_amount: Optional[float] = None
    total_amount: Optional[float] = None
    line_items: List[LineItem] = []

    if response.get('ExpenseDocuments'):
        expense_document = response['ExpenseDocuments'][0]

        # Extract summary fields
        for summary_field in expense_document.get('SummaryFields', []):
            if summary_field.get('Type', {}).get('Text') == 'VENDOR_NAME':
                merchant_name = summary_field.get('ValueDetection', {}).get('Text')
            elif summary_field.get('Type', {}).get('Text') == 'TOTAL':
                try:
                    total_amount = float(summary_field.get('ValueDetection', {}).get('Text'))
                except (ValueError, TypeError):
                    total_amount = None
            elif summary_field.get('Type', {}).get('Text') == 'TAX':
                try:
                    tax_amount = float(summary_field.get('ValueDetection', {}).get('Text'))
                except (ValueError, TypeError):
                    tax_amount = None

        # Extract line items
        for line_item_group in expense_document.get('LineItemGroups', []):
            for item in line_item_group.get('LineItems', []):
                description: Optional[str] = None
                quantity: Optional[float] = None
                price: Optional[float] = None
                total_price: Optional[float] = None

                for field in item.get('LineItemExpenseFields', []):
                    if field.get('Type', {}).get('Text') == 'ITEM':
                        description = field.get('ValueDetection', {}).get('Text')
                    elif field.get('Type', {}).get('Text') == 'QUANTITY':
                        try:
                            quantity = float(field.get('ValueDetection', {}).get('Text'))
                        except (ValueError, TypeError):
                            quantity = None
                    elif field.get('Type', {}).get('Text') == 'PRICE':
                        try:
                            price = float(field.get('ValueDetection', {}).get('Text'))
                        except (ValueError, TypeError):
                            price = None
                    elif field.get('Type', {}).get('Text') == 'TOTAL':
                        try:
                            total_price = float(field.get('ValueDetection', {}).get('Text'))
                        except (ValueError, TypeError):
                            total_price = None
                line_items.append(LineItem(description=description, quantity=quantity, unit_price=price, total_price=total_price))

    # For receipts, we can map merchant_name to vendor_name for consistency with DocumentExtractionResult
    return DocumentExtractionResult(
        vendor_name=merchant_name,
        total_amount=total_amount,
        line_items=line_items,
        raw_response=response
    )
