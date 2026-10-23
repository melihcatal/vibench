from typing import Dict, Any
from datetime import date
from document_models import NormalizedExpense, LineItem


def normalize_expense(
    extracted_data: Dict[str, Any], document_type: str
) -> NormalizedExpense:
    line_items = []
    for item in extracted_data.get("line_items", []):
        line_items.append(
            LineItem(
                description=item.get("description"),
                quantity=item.get("quantity"),
                unit_price=item.get("unit_price"),
                total_price=item.get("total_price"),
            )
        )

    transaction_date = extracted_data.get("transaction_date")
    if isinstance(transaction_date, str):
        try:
            transaction_date = date.fromisoformat(transaction_date)
        except ValueError:
            transaction_date = None
    elif isinstance(transaction_date, date):
        pass  # Already a date object
    else:
        transaction_date = None

    return NormalizedExpense(
        document_type=document_type,
        vendor_name=extracted_data.get("vendor_name")
        or extracted_data.get("merchant_name"),
        transaction_date=transaction_date,
        total_amount=extracted_data.get("total_amount"),
        currency=extracted_data.get("currency"),
        tax_amount=extracted_data.get("tax_amount"),
        line_items=line_items,
        raw_text=extracted_data.get("raw_text"),
        document_id=extracted_data.get("document_id"),
    )
