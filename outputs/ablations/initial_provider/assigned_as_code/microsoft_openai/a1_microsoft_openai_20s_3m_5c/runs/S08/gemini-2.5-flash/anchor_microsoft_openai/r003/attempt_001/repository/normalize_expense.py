import requests
from datetime import datetime
from document_models import ExtractedInvoice, ExtractedReceipt, NormalizedExpense
import uuid
import os


def normalize_expense(extracted_data: dict, document_type: str, config: dict = None) -> NormalizedExpense:
    config = config or {}
    api_key = os.environ.get("FREE_CURRENCY_CONVERTER_API_KEY", config.get("currency_api_key"))
    if not api_key:
        raise ValueError("Missing FREE_CURRENCY_CONVERTER_API_KEY environment variable or config value for currency conversion.")

    transaction_id = str(uuid.uuid4())
    vendor_merchant_name = None
    transaction_date = None
    total_amount = 0.0
    currency = "USD"  # Default currency
    tax_amount = None
    line_items = []

    if document_type == "invoice":
        invoice = ExtractedInvoice(**extracted_data)
        vendor_merchant_name = invoice.vendor
        transaction_date = invoice.date
        total_amount = float(invoice.total) if invoice.total else 0.0
        # Assuming currency is embedded or default
        line_items = [item.model_dump() for item in invoice.line_items]

    elif document_type == "receipt":
        receipt = ExtractedReceipt(**extracted_data)
        vendor_merchant_name = receipt.merchant
        # Receipts often don't have explicit dates, trying to parse from total
        # For now, let's assume date is provided externally or try to infer.
        # For simplicity, using current date if not available.
        transaction_date = datetime.now().strftime("%Y-%m-%d")
        total_amount = float(receipt.total) if receipt.total else 0.0
        tax_amount = float(receipt.tax) if receipt.tax else None
        line_items = [item.model_dump() for item in receipt.items]

    # Example of currency conversion (assuming all amounts are in the same currency as total_amount)
    # For this example, let's assume extracted currency is also 'USD' and convert to 'EUR' if needed.
    # In a real scenario, currency would be extracted from the document.
    target_currency = config.get("target_currency", "USD")
    if currency != target_currency and total_amount > 0:
        query = f"{currency}_{target_currency}"
        url = f"https://free.currencyconverterapi.com/api/v6/convert?q={query}&compact=ultra&apiKey={api_key}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        exchange_rate = data.get(query)
        if exchange_rate:
            total_amount *= exchange_rate
            if tax_amount is not None:
                tax_amount *= exchange_rate
            currency = target_currency


    normalized_expense = NormalizedExpense(
        transaction_id=transaction_id,
        document_type=document_type,
        vendor_merchant_name=vendor_merchant_name or "Unknown",
        transaction_date=transaction_date or datetime.now().strftime("%Y-%m-%d"),
        total_amount=round(total_amount, 2),
        currency=currency,
        tax_amount=round(tax_amount, 2) if tax_amount is not None else None,
        line_items=line_items,
        extracted_raw_data=extracted_data,
        confidence_score=0.0 # This should be set by a validation step
    )
    return normalized_expense
