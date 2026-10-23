import os
import base64
import boto3
from document_client import get_textract_client
from document_models import DocumentInput, ReceiptFields, ReceiptItem

def extract_receipt_fields(document_input: DocumentInput) -> ReceiptFields:
    textract_client = get_textract_client()

    image_bytes = base64.b64decode(document_input.base64_image)

    response = textract_client.analyze_expense(
        Document={
            'Bytes': image_bytes
        }
    )

    merchant_name = ""
    tax_amount = 0.0
    total_amount = 0.0
    currency = ""
    items = []

    for expense_document in response.get('ExpenseDocuments', []):
        for field in expense_document.get('SummaryFields', []):
            if field.get('Type', {}).get('Text') == 'MERCHANT_NAME':
                merchant_name = field.get('ValueDetection', {}).get('Text', '')
            elif field.get('Type', {}).get('Text') == 'TOTAL_TAX':
                tax_amount = float(field.get('ValueDetection', {}).get('Text', '0.0'))
                currency = field.get('ValueDetection', {}).get('Currency', '')
            elif field.get('Type', {}).get('Text') == 'TOTAL':
                total_amount = float(field.get('ValueDetection', {}).get('Text', '0.0'))
                currency = currency or field.get('ValueDetection', {}).get('Currency', '')
        
        for line_item_group in expense_document.get('LineItemGroups', []):
            for line_item in line_item_group.get('LineItems', []):
                item_description = ""
                item_price = 0.0
                item_quantity = 0
                item_total = 0.0
                
                for field in line_item.get('LineItemFields', []):
                    if field.get('Type', {}).get('Text') == 'ITEM':
                        item_description = field.get('ValueDetection', {}).get('Text', '')
                    elif field.get('Type', {}).get('Text') == 'PRICE':
                        item_price = float(field.get('ValueDetection', {}).get('Text', '0.0'))
                    elif field.get('Type', {}).get('Text') == 'QUANTITY':
                        item_quantity = int(float(field.get('ValueDetection', {}).get('Text', '0')))
                    elif field.get('Type', {}).get('Text') == 'TOTAL':
                        item_total = float(field.get('ValueDetection', {}).get('Text', '0.0'))
                
                items.append(ReceiptItem(
                    description=item_description,
                    price=item_price,
                    quantity=item_quantity,
                    total=item_total
                ))

    return ReceiptFields(
        merchant_name=merchant_name,
        tax_amount=tax_amount,
        total_amount=total_amount,
        currency=currency,
        items=items
    )
