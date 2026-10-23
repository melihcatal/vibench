import base64
from typing import Optional, List, Dict, Any
from document_client import get_textract_client
from document_models import InvoiceExtractionResult, LineItem

def extract_invoice_fields(document_bytes: bytes) -> InvoiceExtractionResult:
    """
    Extracts vendor, date, total, and line-item fields from an invoice using AWS Textract's AnalyzeExpense.
    """
    textract_client = get_textract_client()

    response = textract_client.analyze_expense(
        Document={'Bytes': document_bytes}
    )

    vendor_name: Optional[str] = None
    invoice_date: Optional[str] = None
    invoice_total: Optional[float] = None
    line_items: List[LineItem] = []

    if response.get('ExpenseDocuments'):
        for expense_doc in response['ExpenseDocuments']:
            if expense_doc.get('SummaryFields'):
                for field in expense_doc['SummaryFields']:
                    field_type = field.get('Type', {}).get('Text')
                    if field_type == 'VENDOR_NAME' and 'ValueDetection' in field:
                        vendor_name = field['ValueDetection']['Text']
                    elif field_type == 'DATE' and 'ValueDetection' in field:
                        invoice_date = field['ValueDetection']['Text']
                    elif field_type == 'TOTAL' and 'ValueDetection' in field:
                        try:
                            invoice_total = float(field['ValueDetection']['Text'])
                        except (ValueError, TypeError):
                            invoice_total = None

            if expense_doc.get('LineItemGroups'):
                for item_group in expense_doc['LineItemGroups']:
                    for item in item_group.get('LineItems', []):
                        item_description: Optional[str] = None
                        item_quantity: Optional[float] = None
                        item_unit_price: Optional[float] = None
                        item_amount: Optional[float] = None

                        for field in item.get('LineItemExpenseFields', []):
                            field_type = field.get('Type', {}).get('Text')
                            if field_type == 'ITEM_DESCRIPTION' and 'ValueDetection' in field:
                                item_description = field['ValueDetection']['Text']
                            elif field_type == 'QUANTITY' and 'ValueDetection' in field:
                                try:
                                    item_quantity = float(field['ValueDetection']['Text'])
                                except (ValueError, TypeError):
                                    item_quantity = None
                            elif field_type == 'UNIT_PRICE' and 'ValueDetection' in field:
                                try:
                                    item_unit_price = float(field['ValueDetection']['Text'])
                                except (ValueError, TypeError):
                                    item_unit_price = None
                            elif field_type == 'PRICE' and 'ValueDetection' in field:
                                try:
                                    item_amount = float(field['ValueDetection']['Text'])
                                except (ValueError, TypeError):
                                    item_amount = None

                        if item_description or item_amount is not None:
                            line_items.append({
                                'description': item_description if item_description is not None else "Unknown",
                                'quantity': item_quantity,
                                'unit_price': item_unit_price,
                                'amount': item_amount if item_amount is not None else 0.0
                            })
            break

    return {
        'vendor_name': vendor_name,
        'invoice_date': invoice_date,
        'invoice_total': invoice_total,
        'line_items': line_items,
        'raw_data': response
    }
