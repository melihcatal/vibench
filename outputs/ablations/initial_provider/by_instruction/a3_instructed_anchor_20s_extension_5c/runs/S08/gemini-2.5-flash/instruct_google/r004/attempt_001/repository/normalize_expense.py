from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from document_models import Invoice, Receipt, LineItem

@dataclass
class NormalizedExpenseItem:
    description: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total_price: Optional[float] = None

@dataclass
class NormalizedExpense:
    document_type: str # "invoice" or "receipt"
    vendor_merchant_name: Optional[str] = None
    transaction_date: Optional[str] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    tax_amount: Optional[float] = None # Primarily for receipts, but can be present in invoices
    items: List[NormalizedExpenseItem] = field(default_factory=list)

def normalize_expense(document_data: Any) -> Dict[str, Any]:
    if isinstance(document_data, Invoice):
        normalized_items = [
            NormalizedExpenseItem(
                description=item.description,
                quantity=item.quantity,
                unit_price=item.unit_price,
                total_price=item.total_price
            ) for item in document_data.line_items
        ]
        normalized_expense = NormalizedExpense(
            document_type="invoice",
            vendor_merchant_name=document_data.vendor_name,
            transaction_date=document_data.invoice_date,
            total_amount=document_data.total_amount,
            currency=document_data.currency,
            items=normalized_items
        )
    elif isinstance(document_data, Receipt):
        normalized_items = [
            NormalizedExpenseItem(
                description=item.description,
                quantity=item.quantity,
                unit_price=item.unit_price,
                total_price=item.total_price
            ) for item in document_data.items
        ]
        normalized_expense = NormalizedExpense(
            document_type="receipt",
            vendor_merchant_name=document_data.merchant_name,
            transaction_date=document_data.transaction_date,
            total_amount=document_data.total_amount,
            currency=document_data.currency,
            tax_amount=document_data.tax_amount,
            items=normalized_items
        )
    else:
        raise ValueError("Unsupported document_data type. Must be Invoice or Receipt.")

    return asdict(normalized_expense)
