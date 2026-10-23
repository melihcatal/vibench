from document_client import get_textract_client
import json

def extract_invoice_fields(document_bytes: bytes) -> dict:
    """
    Extracts vendor, date, total, and line-item fields from an invoice using AWS Textract.

    Args:
        document_bytes: The byte content of the invoice document.

    Returns:
        A dictionary containing extracted invoice fields.
    """
    textract_client = get_textract_client()
    response = textract_client.analyze_expense(Document={'Bytes': document_bytes})

    extracted_fields = {
        "vendor_name": None,
        "invoice_date": None,
        "total_amount": None,
        "line_items": []
    }

    for expense_document in response.get('ExpenseDocuments', []):
        # Extract general fields
        for field in expense_document.get('SummaryFields', []):
            field_type = field.get('Type', {}).get('Text')
            if field_type == 'VENDOR_NAME':
                extracted_fields['vendor_name'] = field.get('ValueDetection', {}).get('Text')
            elif field_type == 'DATE':
                extracted_fields['invoice_date'] = field.get('ValueDetection', {}).get('Text')
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
                    extracted_fields['line_items'].append(item)

    return extracted_fields
