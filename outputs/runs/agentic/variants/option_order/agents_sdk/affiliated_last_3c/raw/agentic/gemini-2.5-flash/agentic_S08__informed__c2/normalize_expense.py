from document_models import NormalizedExpense, LineItem
from typing import Dict, Any, List, Optional

def normalize_expense_data(
    document_type: str,
    extracted_data: Dict[str, Any],
    raw_document_path: Optional[str] = None
) -> NormalizedExpense:
    """
    Normalizes extracted expense fields into a standard NormalizedExpense JSON schema.

    Args:
        document_type: The type of the document (e.g., "invoice", "receipt").
        extracted_data: A dictionary containing the raw extracted fields.
                        Expected keys: 'vendor_name', 'transaction_date', 'total_amount',
                        'tax_amount', 'currency', 'line_items', 'confidence_scores', 'notes'.
        raw_document_path: Optional path or URL to the original document.
    """
    line_items: List[LineItem] = []
    if 'line_items' in extracted_data and isinstance(extracted_data['line_items'], list):
        for item in extracted_data['line_items']:
            line_items.append(LineItem(
                description=item.get('description'),
                quantity=item.get('quantity'),
                unit_price=item.get('unit_price'),
                amount=item.get('amount')
            ))

    return NormalizedExpense(
        document_type=document_type,
        vendor_name=extracted_data.get('vendor_name'),
        transaction_date=extracted_data.get('transaction_date'),
        total_amount=extracted_data.get('total_amount'),
        tax_amount=extracted_data.get('tax_amount'),
        currency=extracted_data.get('currency'),
        line_items=line_items,
        confidence_scores=extracted_data.get('confidence_scores', {}),
        raw_document_path=raw_document_path,
        notes=extracted_data.get('notes')
    )
