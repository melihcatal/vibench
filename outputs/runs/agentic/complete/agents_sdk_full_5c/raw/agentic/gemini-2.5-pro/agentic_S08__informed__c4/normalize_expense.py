from typing import List, Optional
from azure.ai.documentintelligence.models import AnalyzeResult
from document_models import NormalizedExpense, LineItem
import uuid

def _get_field_value(document, field_name):
    field = document.fields.get(field_name)
    if field:
        return field.value
    return None

def normalize_expense_from_azure(result: AnalyzeResult, source_file: str) -> Optional[NormalizedExpense]:
    """
    Normalizes the output from Azure Document Intelligence into a standard schema.
    """
    if not result.documents or len(result.documents) == 0:
        return None

    document = result.documents[0]
    
    # Handle different field names for vendor/merchant
    vendor_name = _get_field_value(document, "VendorName") or _get_field_value(document, "MerchantName")
    
    # Handle different field names for date
    transaction_date = _get_field_value(document, "InvoiceDate") or _get_field_value(document, "TransactionDate")

    # Handle different field names for total
    total = _get_field_value(document, "InvoiceTotal") or _get_field_value(document, "Total")
    if total:
        total = total.amount if hasattr(total, 'amount') else total

    tax = _get_field_value(document, "TotalTax")
    if tax:
        tax = tax.amount if hasattr(tax, 'amount') else tax

    items_field = document.fields.get("Items") or document.fields.get("InvoiceItems")
    line_items: List[LineItem] = []
    
    if items_field and items_field.value_array:
        for item in items_field.value_array:
            if item.value_object:
                line_item_data = {
                    'description': _get_field_value(item.value_object, "Description"),
                    'quantity': _get_field_value(item.value_object, "Quantity"),
                    'unit_price': getattr(_get_field_value(item.value_object, "UnitPrice"), 'amount', None),
                    'total_amount': getattr(_get_field_value(item.value_object, "Amount"), 'amount', None) or getattr(_get_field_value(item.value_object, "LineTotal"), 'amount', None),
                }
                line_items.append(LineItem(**line_item_data))

    return NormalizedExpense(
        expense_id=str(uuid.uuid4()),
        source_file=source_file,
        vendor=vendor_name,
        transaction_date=transaction_date,
        total=total,
        tax=tax,
        line_items=line_items,
    )
