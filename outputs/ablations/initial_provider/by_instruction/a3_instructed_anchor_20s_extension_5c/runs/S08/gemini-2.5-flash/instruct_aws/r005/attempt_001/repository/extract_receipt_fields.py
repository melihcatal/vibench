from document_client import get_textract_client
import json

def extract_receipt_fields(document_bytes: bytes) -> dict:
    """
    Extracts merchant, tax, total, and items from a receipt using AWS Textract.

    Args:
        document_bytes: The byte content of the receipt document.

    Returns:
        A dictionary containing extracted receipt fields.
    """
    textract_client = get_textract_client()
    response = textract_client.analyze_expense(Document={'Bytes': document_bytes})

    extracted_fields = {
        "merchant_name": None,
        "tax_amount": None,
        "total_amount": None,
        "items": []
    }

    for expense_document in response.get('ExpenseDocuments', []):
        # Extract general fields
        for field in expense_document.get('SummaryFields', []):
            field_type = field.get('Type', {}).get('Text')
            if field_type == 'VENDOR_NAME': # Merchant name is often under VENDOR_NAME for receipts
                extracted_fields['merchant_name'] = field.get('ValueDetection', {}).get('Text')
            elif field_type == 'TOTAL_TAX':
                extracted_fields['tax_amount'] = field.get('ValueDetection', {}).get('Text')
            elif field_type == 'TOTAL':
                extracted_fields['total_amount'] = field.get('ValueDetection', {}).get('Text')

        # Extract line items
        for line_item_group in expense_document.get('LineItemGroups', []):
            for line_item in line_item_group.get('LineItems', []):
                item = {}
                for field in line_item.get('LineItemExpenseFields', []):
                    field_type = field.get('Type', {}).get('Text')
                    if field_type == 'ITEM':
                        item['description'] = field.get('ValueDetection', {}).get('Text')
                    elif field_type == 'PRICE':
                        item['price'] = field.get('ValueDetection', {}).get('Text')
                    elif field_type == 'QUANTITY':
                        item['quantity'] = field.get('ValueDetection', {}).get('Text')
                if item:
                    extracted_fields['items'].append(item)

    return extracted_fields
