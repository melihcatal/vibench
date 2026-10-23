from typing import Dict, Any, List
from document_models import NormalizedExpense, LineItem

def normalize_expense(extracted_data: Dict[str, Any], document_type: str) -> NormalizedExpense:
    """
    Normalizes extracted expense fields into a standard JSON schema.
    document_type can be 'invoice' or 'receipt'.
    """
    normalized_items: List[LineItem] = []
    for item in extracted_data.get("line_items", []):
        normalized_items.append(LineItem(
            description=item.get("description", ""),
            quantity=float(item.get("quantity", 0)) if item.get("quantity") else 0.0,
            unit_price=float(item.get("unit_price", 0)) if item.get("unit_price") else 0.0,
            amount=float(item.get("amount", 0)) if item.get("amount") else 0.0,
        ))
    
    vendor_name = ""
    transaction_date = ""
    total_amount = 0.0
    tax_amount = 0.0

    if document_type == 'invoice':
        vendor_name = extracted_data.get("vendor_name", "")
        transaction_date = extracted_data.get("invoice_date", "")
        total_amount = float(extracted_data.get("total_amount", 0)) if extracted_data.get("total_amount") else 0.0
    elif document_type == 'receipt':
        vendor_name = extracted_data.get("merchant_name", "")
        transaction_date = extracted_data.get("transaction_date", "") # Receipts might have this field
        total_amount = float(extracted_data.get("total_amount", 0)) if extracted_data.get("total_amount") else 0.0
        tax_amount = float(extracted_data.get("tax_amount", 0)) if extracted_data.get("tax_amount") else 0.0

    return NormalizedExpense(
        document_type=document_type,
        vendor_name=vendor_name,
        transaction_date=transaction_date,
        total_amount=total_amount,
        tax_amount=tax_amount,
        line_items=normalized_items,
        raw_extraction=extracted_data # Store the original for auditing/debugging
    )

if __name__ == '__main__':
    # Example Usage for Invoice
    invoice_data = {
        "vendor_name": "Example Corp",
        "invoice_date": "2023-10-27",
        "total_amount": "150.75",
        "line_items": [
            {"description": "Item A", "quantity": "1", "unit_price": "100.00", "amount": "100.00"},
            {"description": "Item B", "quantity": "2", "unit_price": "25.00", "amount": "50.00"}
        ]
    }
    normalized_invoice = normalize_expense(invoice_data, "invoice")
    print("Normalized Invoice:", normalized_invoice.model_dump_json(indent=2))

    print("\n"+"-"*30+"\n")

    # Example Usage for Receipt
    receipt_data = {
        "merchant_name": "Coffee Shop",
        "transaction_date": "2023-10-27",
        "total_amount": "12.50",
        "tax_amount": "0.75",
        "line_items": [
            {"description": "Latte", "quantity": "1", "unit_price": "5.50", "amount": "5.50"},
            {"description": "Muffin", "quantity": "1", "unit_price": "4.00", "amount": "4.00"}
        ]
    }
    normalized_receipt = normalize_expense(receipt_data, "receipt")
    print("Normalized Receipt:", normalized_receipt.model_dump_json(indent=2))
