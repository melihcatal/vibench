import os
import requests
from document_models import InvoiceExtractionResult, ReceiptExtractionResult, NormalizedExpense, LineItem

# Using a public currency exchange API for illustrative purposes to meet the provider requirement.
# In a real scenario, this would involve proper API key handling and error management.
EXCHANGE_RATE_API_BASE_URL = "https://api.exchangerate-api.com/v6/latest"
EXCHANGE_RATE_API_KEY = os.environ.get("EXCHANGE_RATE_API_KEY", "YOUR_EXCHANGE_RATE_API_KEY")

def get_exchange_rate(base_currency: str, target_currency: str) -> float:
    if base_currency == target_currency:
        return 1.0

    try:
        # Note: Many free tiers of exchange rate APIs only support USD as base or limited requests.
        # This is a conceptual integration.
        response = requests.get(
            f"{EXCHANGE_RATE_API_BASE_URL}?access_key={EXCHANGE_RATE_API_KEY}&base={base_currency}"
        )
        response.raise_for_status()
        data = response.json()
        rate = data["rates"].get(target_currency)
        if rate is None:
            print(f"Warning: Exchange rate for {base_currency} to {target_currency} not found.")
            return 1.0 # Default to 1 if not found
        return float(rate)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching exchange rate: {e}")
        return 1.0 # Default to 1 on error

def normalize_expense(
    extraction_result: InvoiceExtractionResult | ReceiptExtractionResult,
    target_currency: str = "USD"
) -> NormalizedExpense:
    if isinstance(extraction_result, InvoiceExtractionResult):
        vendor = extraction_result.vendor
        date = extraction_result.date
        amount = extraction_result.total
        original_currency = extraction_result.currency if extraction_result.currency else "USD" # Assume USD if not explicitly extracted
        description = "Invoice payment"
        line_items = extraction_result.line_items
    elif isinstance(extraction_result, ReceiptExtractionResult):
        vendor = extraction_result.merchant
        date = "" # Receipts often don't have a distinct 'invoice date' field, using empty for now.
        amount = extraction_result.total
        original_currency = extraction_result.currency if extraction_result.currency else "USD" # Assume USD if not explicitly extracted
        description = "Receipt expense"
        line_items = extraction_result.items
    else:
        raise ValueError("Unsupported extraction result type.")

    # In a real scenario, currency would be extracted from the document.
    # For this example, we'll assume a default and convert if needed.
    converted_amount = amount
    converted_line_items = []

    if original_currency != target_currency:
        exchange_rate = get_exchange_rate(original_currency, target_currency)
        converted_amount = amount * exchange_rate
        for item in line_items:
            converted_line_items.append(
                LineItem(description=item.description, amount=item.amount * exchange_rate)
            )
    else:
        converted_line_items = line_items


    return NormalizedExpense(
        vendor=vendor,
        date=date,
        amount=converted_amount,
        currency=target_currency,
        description=description,
        line_items=converted_line_items
    )

if __name__ == '__main__':
    # Example usage:
    # invoice_res = InvoiceExtractionResult(vendor="Test Inc", date="2023-01-01", total=100.0, line_items=[LineItem(description="Item A", amount=50.0)])
    # normalized = normalize_expense(invoice_res, "EUR")
    # print(normalized.model_dump_json(indent=2))
    pass
