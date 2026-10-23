"""
Extracts merchant, tax, total, and items from a receipt using AWS Textract.
"""
from document_client import get_aws_textract_client
from document_models import Receipt, LineItem

def get_field_value(fields, field_name):
    """Helper to extract value from Textract expense fields."""
    for field in fields:
        if field.get("Type", {}).get("Text") == field_name:
            return field.get("ValueDetection", {}).get("Text")
    return None

def extract_receipt(file_path: str) -> Receipt:
    """
    Extracts structured data from a receipt document using AnalyzeExpense.
    """
    textract_client = get_aws_textract_client()

    with open(file_path, "rb") as document:
        response = textract_client.analyze_expense(
            Document={"Bytes": document.read()}
        )
    
    if not response.get("ExpenseDocuments"):
        return Receipt(merchant_name=None, transaction_date=None, tax=None, total=None)

    expense = response["ExpenseDocuments"][0]
    summary_fields = expense.get("SummaryFields", [])
    line_item_groups = expense.get("LineItemGroups", [])

    merchant_name = get_field_value(summary_fields, "VENDOR_NAME")
    transaction_date = get_field_value(summary_fields, "INVOICE_RECEIPT_DATE")
    tax_str = get_field_value(summary_fields, "TAX")
    total_str = get_field_value(summary_fields, "TOTAL")

    items = []
    for group in line_item_groups:
        for item in group.get("LineItems", []):
            line_item_fields = item.get("LineItemExpenseFields", [])
            description = get_field_value(line_item_fields, "ITEM")
            price = get_field_value(line_item_fields, "PRICE")
            qty = get_field_value(line_item_fields, "QUANTITY")
            
            items.append(LineItem(
                description=description,
                quantity=float(qty) if qty else None,
                total_amount=float(price.replace('$', '')) if price else None,
                unit_price=None # Not always available in AnalyzeExpense
            ))

    return Receipt(
        merchant_name=merchant_name,
        transaction_date=transaction_date,
        tax=float(tax_str.replace('$', '')) if tax_str else None,
        total=float(total_str.replace('$', '')) if total_str else None,
        items=items,
    )
