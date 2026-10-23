import os
import requests
from document_models import Invoice, Receipt, NormalizedExpense

API_KEY = os.environ.get("EXCHANGERATESAPI_IO_API_KEY")
API_URL = "http://api.exchangeratesapi.io/v1/latest"


def normalize_expense(
    expense_doc: (Invoice | Receipt), target_currency: str = "USD"
) -> NormalizedExpense:
    if isinstance(expense_doc, Invoice):
        vendor = expense_doc.vendor_name
        transaction_date = expense_doc.invoice_date
        total = expense_doc.total_amount
        items = [item.dict() for item in expense_doc.line_items]
        doc_type = "invoice"
    elif isinstance(expense_doc, Receipt):
        vendor = expense_doc.merchant_name
        transaction_date = expense_doc.transaction_date
        total = expense_doc.total_amount
        items = [item.dict() for item in expense_doc.items]
        doc_type = "receipt"
    else:
        raise TypeError("Unsupported document type for normalization")

    # Assuming source currency is USD, convert if needed
    final_total = total
    if target_currency != "USD":
        if not API_KEY:
            raise ValueError(
                "EXCHANGERATESAPI_IO_API_KEY must be set for currency conversion."
            )

        params = {"access_key": API_KEY, "symbols": target_currency}
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        rates = response.json().get("rates", {})

        if target_currency in rates:
            final_total = total * rates[target_currency]
        else:
            raise ValueError(f"Currency {target_currency} not supported by API.")

    return NormalizedExpense(
        vendor=vendor,
        transaction_date=transaction_date,
        total=final_total,
        currency=target_currency,
        items=items,
        source_document_type=doc_type,
        source_document_confidence=expense_doc.confidence,
    )
