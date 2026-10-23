import os
from typing import Union, List
import requests
from document_models import Invoice, Receipt, NormalizedExpense, NormalizedExpenseItem

EXCHANGE_RATE_API_URL = os.environ.get("EXCHANGE_RATE_API_URL", "https://api.exchangerate.host/latest")
BASE_CURRENCY = os.environ.get("BASE_CURRENCY", "USD")

def get_exchange_rate(from_currency: str, to_currency: str) -> float:
    """Fetches the exchange rate between two currencies using an external API."""
    if from_currency == to_currency:
        return 1.0
    try:
        response = requests.get(EXCHANGE_RATE_API_URL, params={'base': from_currency, 'symbols': to_currency})
        response.raise_for_status()
        data = response.json()
        rate = data['rates'].get(to_currency)
        if rate is None:
            raise ValueError(f"Could not find exchange rate for {from_currency} to {to_currency}")
        return rate
    except requests.exceptions.RequestException as e:
        print(f"Error fetching exchange rate: {e}")
        return 1.0 # Default to 1.0 on error, or raise
    except ValueError as e:
        print(f"Error parsing exchange rate data: {e}")
        return 1.0 # Default to 1.0 on error, or raise

def normalize_expense(document: Union[Invoice, Receipt]) -> NormalizedExpense:
    """Normalizes extracted expense fields into a standard JSON schema.

    Args:
        document: An Invoice or Receipt dataclass instance.

    Returns:
        A NormalizedExpense dataclass instance.
    """

    normalized_items: List[NormalizedExpenseItem] = []
    total_expense = 0.0
    total_tax = 0.0
    source_document_type = ""
    primary_vendor_merchant = None
    transaction_date = None
    original_currency = None
    source_document_id = document.document_id

    if isinstance(document, Invoice):
        source_document_type = "invoice"
        primary_vendor_merchant = document.vendor_name
        transaction_date = document.invoice_date
        original_currency = document.currency
        items_to_process = document.line_items
        total_expense = document.total_amount if document.total_amount is not None else 0.0
        # Invoices typically don't have a separate 'tax_amount' field at the top level in this model
    elif isinstance(document, Receipt):
        source_document_type = "receipt"
        primary_vendor_merchant = document.merchant_name
        transaction_date = document.transaction_date
        original_currency = document.currency
        items_to_process = document.items
        total_expense = document.total_amount if document.total_amount is not None else 0.0
        total_tax = document.tax_amount if document.tax_amount is not None else 0.0

    # Convert total amounts to base currency if needed
    conversion_rate = 1.0
    if original_currency and original_currency != BASE_CURRENCY:
        conversion_rate = get_exchange_rate(original_currency, BASE_CURRENCY)
        total_expense *= conversion_rate
        total_tax *= conversion_rate

    for item in items_to_process:
        item_total = item.total_amount if item.total_amount is not None else 0.0
        item_total_converted = item_total * conversion_rate
        normalized_items.append(NormalizedExpenseItem(
            description=item.description,
            quantity=item.quantity,
            unit_price=item.unit_price,
            total_amount=item_total_converted,
            currency=BASE_CURRENCY
        ))

    return NormalizedExpense(
        source_document_type=source_document_type,
        primary_vendor_merchant=primary_vendor_merchant,
        transaction_date=transaction_date,
        total_expense_amount=round(total_expense, 2) if total_expense is not None else None,
        total_tax_amount=round(total_tax, 2) if total_tax is not None else None,
        standardized_currency=BASE_CURRENCY,
        expense_items=normalized_items,
        source_document_id=source_document_id,
        notes=None, # Populated by other steps if applicable
        validation_status={}
    )
