from typing import Union, Dict, Any
from document_models import InvoiceDocument, ReceiptDocument, NormalizedExpense

def normalize_expense(document: Union[InvoiceDocument, ReceiptDocument]) -> NormalizedExpense:
    """Normalizes extracted invoice or receipt fields into a standard JSON schema (NormalizedExpense).

    Args:
        document: An InvoiceDocument or ReceiptDocument object.

    Returns:
        A NormalizedExpense object.
    """
    confidence_scores: Dict[str, float] = {}

    if isinstance(document, InvoiceDocument):
        document_type = "invoice"
        vendor_merchant_name = document.vendor_name
        transaction_date = document.invoice_date
        total_amount = document.total_amount
        currency = document.currency
        tax_amount = None
        line_items = []

        if document.raw_textract_output:
            # Example: Extract confidence for vendor name from raw Textract output
            # This is a simplified approach, a real implementation would traverse the blocks
            # to find confidence of specific fields.
            for block in document.raw_textract_output.get('Blocks', []):
                if block['BlockType'] == 'WORD' and document.vendor_name and document.vendor_name in block['Text']:
                    confidence_scores['vendor_name'] = block['Confidence']
                    break
            # More confidence scores can be added here for date, total, etc.

        for item in document.line_items:
            line_item_data = {}
            for field in item.fields:
                if field.name and field.value:
                    line_item_data[field.name.lower().replace(' ', '_')] = field.value
                    if field.confidence:
                        confidence_scores[f'line_item_{field.name.lower().replace(' ', '_')}_confidence'] = field.confidence
            if line_item_data:
                line_items.append(line_item_data)


    elif isinstance(document, ReceiptDocument):
        document_type = "receipt"
        vendor_merchant_name = document.merchant_name
        transaction_date = document.transaction_date
        total_amount = document.total_amount
        currency = document.currency
        tax_amount = document.tax_amount
        line_items = []

        if document.raw_textract_output:
            # Example: Extract confidence for merchant name from raw Textract output
            for expense_doc in document.raw_textract_output.get('ExpenseDocuments', [])[:1]: # Take the first one
                for field in expense_doc.get('SummaryFields', []):
                    field_type = field.get('Type', {}).get('Text')
                    if field_type == 'MERCHANT_NAME' and field.get('ValueDetection', {}).get('Confidence') is not None:
                        confidence_scores['merchant_name'] = field['ValueDetection']['Confidence']
                    elif field_type == 'TOTAL' and field.get('ValueDetection', {}).get('Confidence') is not None:
                        confidence_scores['total_amount'] = field['ValueDetection']['Confidence']
                    elif field_type == 'TAX' and field.get('ValueDetection', {}).get('Confidence') is not None:
                        confidence_scores['tax_amount'] = field['ValueDetection']['Confidence']
                    elif field_type == 'DATE' and field.get('ValueDetection', {}).get('Confidence') is not None:
                        confidence_scores['transaction_date'] = field['ValueDetection']['Confidence']

                for item_group in expense_doc.get('LineItemGroups', [])[:1]:
                    for item in item_group.get('LineItems', [])[:1]:
                        for field in item.get('LineItemExpenseFields', []):
                            if field.get('ValueDetection', {}).get('Confidence') is not None:
                                confidence_scores[f'line_item_{field.get('Type', {}).get('Text', '').lower().replace(' ', '_')}_confidence'] = field['ValueDetection']['Confidence']

        for item in document.line_items:
            line_item_data = {}
            for field in item.fields:
                if field.name and field.value:
                    line_item_data[field.name.lower().replace(' ', '_')] = field.value
                    if field.confidence:
                        confidence_scores[f'line_item_{field.name.lower().replace(' ', '_')}_confidence'] = field.confidence
            if line_item_data:
                line_items.append(line_item_data)

    else:
        raise ValueError("Unsupported document type.")

    return NormalizedExpense(
        document_type=document_type,
        vendor_merchant_name=vendor_merchant_name,
        transaction_date=transaction_date,
        total_amount=total_amount,
        currency=currency,
        tax_amount=tax_amount,
        line_items=line_items,
        confidence_scores=confidence_scores,
        original_extracted_data=document.raw_textract_output if document.raw_textract_output else {}
    )
