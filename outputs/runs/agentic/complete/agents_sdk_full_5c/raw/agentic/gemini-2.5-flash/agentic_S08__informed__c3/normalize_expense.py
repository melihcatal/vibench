"""
normalize_expense.py

Normalizes extracted expense fields into a standard JSON schema (Expense model).
"""

from typing import Dict, Any, Optional, List
from datetime import date
from document_models import Expense, LineItem

def normalize_expense(document_type: str, extracted_fields: Dict[str, Any]) -> Expense:
    """
    Normalizes extracted fields from an invoice or receipt into a standard Expense object.

    Args:
        document_type: Either 'invoice' or 'receipt'.
        extracted_fields: A dictionary of fields extracted by a document parser.

    Returns:
        An Expense object with normalized fields.
    """
    vendor_name: Optional[str] = None
    transaction_date: Optional[date] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    tax_amount: Optional[float] = None
    line_items: List[LineItem] = []
    notes: Optional[str] = None

    if document_type == 'invoice':
        vendor_name = extracted_fields.get('vendor_name')
        transaction_date = extracted_fields.get('transaction_date')
        total_amount = extracted_fields.get('total_amount')
        currency = extracted_fields.get('currency')
        notes = extracted_fields.get('notes')
        extracted_line_items = extracted_fields.get('line_items', [])
        for item in extracted_line_items:
            line_items.append(LineItem(
                description=item.description,
                quantity=item.quantity,
                unit_price=item.unit_price,
                amount=item.amount
            ))
    elif document_type == 'receipt':
        vendor_name = extracted_fields.get('merchant_name')
        transaction_date = extracted_fields.get('transaction_date')
        total_amount = extracted_fields.get('total_amount')
        currency = extracted_fields.get('currency')
        tax_amount = extracted_fields.get('tax_amount')
        notes = extracted_fields.get('notes')
        extracted_line_items = extracted_fields.get('line_items', [])
        for item in extracted_line_items:
            line_items.append(LineItem(
                description=item.description,
                quantity=item.quantity,
                unit_price=item.unit_price,
                amount=item.amount
            ))
    else:
        raise ValueError("Invalid document_type. Must be 'invoice' or 'receipt'.")

    return Expense(
        document_type=document_type,
        vendor_name=vendor_name,
        transaction_date=transaction_date,
        total_amount=total_amount,
        currency=currency,
        tax_amount=tax_amount,
        line_items=line_items,
        original_data=extracted_fields, # Store original for reference
        notes=notes
    )
