import os
from typing import Dict, Any, Optional, List
from document_client import get_aws_textract_client
from document_models import ReceiptDocument, LineItem, LineItemField

def extract_receipt_fields(document_s3_path: str) -> ReceiptDocument:
    """Extracts merchant, tax, total, and items from a receipt using AWS Textract AnalyzeExpense.

    Args:
        document_s3_path: S3 path to the receipt document (e.g., "s3://bucket-name/path/to/receipt.pdf")

    Returns:
        A ReceiptDocument object containing the extracted fields and raw Textract output.
    """
    textract_client = get_aws_textract_client()

    bucket_name = document_s3_path.split('/')[2]
    object_name = '/'.join(document_s3_path.split('/')[3:])

    response = textract_client.analyze_expense(
        Document={
            'S3Object': {
                'Bucket': bucket_name,
                'Name': object_name
            }
        }
    )

    extracted_merchant = None
    extracted_date = None
    extracted_total = None
    extracted_tax = None
    extracted_currency = None
    extracted_line_items: List[LineItem] = []

    # AnalyzeExpense response structure is different from AnalyzeDocument
    # It provides a list of ExpenseDocuments, usually one per receipt image
    for expense_doc in response.get('ExpenseDocuments', []):
        # Summary fields
        summary_fields = expense_doc.get('SummaryFields', [])
        for field in summary_fields:
            field_type = field.get('Type', {}).get('Text')
            field_value = field.get('ValueDetection', {}).get('Text')
            field_confidence = field.get('ValueDetection', {}).get('Confidence')

            if field_type == 'MERCHANT_NAME':
                extracted_merchant = field_value
            elif field_type == 'DATE':
                extracted_date = field_value
            elif field_type == 'TOTAL':
                try:
                    extracted_total = float(field_value)
                    if field.get('ValueDetection', {}).get('Currency'):
                        extracted_currency = field.get('ValueDetection', {}).get('Currency')
                except (ValueError, TypeError):
                    pass
            elif field_type == 'TAX':
                try:
                    extracted_tax = float(field_value)
                except (ValueError, TypeError):
                    pass
        
        # Line item fields
        line_item_groups = expense_doc.get('LineItemGroups', [])
        for group in line_item_groups:
            for item in group.get('LineItems', []):
                line_item_fields: List[LineItemField] = []
                for field in item.get('LineItemExpenseFields', []):
                    field_type = field.get('Type', {}).get('Text')
                    field_value = field.get('ValueDetection', {}).get('Text')
                    field_confidence = field.get('ValueDetection', {}).get('Confidence')
                    line_item_fields.append(LineItemField(name=field_type, value=field_value, confidence=field_confidence))
                extracted_line_items.append(LineItem(fields=line_item_fields))

    return ReceiptDocument(
        merchant_name=extracted_merchant,
        transaction_date=extracted_date,
        total_amount=extracted_total,
        tax_amount=extracted_tax,
        currency=extracted_currency,
        line_items=extracted_line_items,
        raw_textract_output=response
    )
