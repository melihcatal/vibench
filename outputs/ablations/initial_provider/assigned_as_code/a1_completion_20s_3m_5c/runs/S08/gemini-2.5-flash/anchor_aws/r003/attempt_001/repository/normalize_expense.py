import os
import requests
from document_models import ExtractedDocumentFields, NormalizedExpense, LineItem
from typing import List, Optional

FIXER_API_KEY = os.environ.get("FIXER_API_KEY")
FIXER_BASE_URL = "http://data.fixer.io/api/latest" # Note: Free tier might only support HTTP, not HTTPS

def normalize_expense(extracted_data: ExtractedDocumentFields, document_type: str = "invoice") -> NormalizedExpense:
    normalized_expense = NormalizedExpense(raw_extraction=extracted_data.dict())

    if document_type == "invoice":
        normalized_expense.vendor_name = extracted_data.vendor
        normalized_expense.transaction_date = extracted_data.date
        normalized_expense.total_amount = float(extracted_data.total) if extracted_data.total else None
        normalized_expense.line_items = extracted_data.line_items
    elif document_type == "receipt":
        normalized_expense.vendor_name = extracted_data.merchant
        normalized_expense.transaction_date = extracted_data.date
        normalized_expense.total_amount = float(extracted_data.total) if extracted_data.total else None
        # Receipts often don't have detailed line items in the same way as invoices,
        # but Textract's analyze_expense provides them under LineItemGroups.
        normalized_expense.line_items = extracted_data.items

    # Basic currency conversion example (assuming extracted data is in a base currency, e.g., USD)
    # This is a placeholder for actual currency extraction and conversion logic.
    if normalized_expense.total_amount and FIXER_API_KEY:
        try:
            params = {"access_key": FIXER_API_KEY, "base": "EUR", "symbols": "USD"} # Fixer.io free tier base is EUR
            response = requests.get(FIXER_BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            if data["success"] and "rates" in data and "USD" in data["rates"]:
                # Assume the extracted total is in EUR for this example (if base currency is EUR)
                # In a real scenario, you'd extract the currency from the document itself.
                # For this example, let's assume conversion *to* USD if the extracted amount is in EUR.
                # This logic is highly simplified and assumes knowing the original currency.
                # A more robust solution would involve detecting the currency from the document.
                normalized_expense.currency = "USD"
                # For now, let's just show the rate without actual conversion, as we don't know input currency.
                # normalized_expense.total_amount = normalized_expense.total_amount * eur_to_usd_rate
            else:
                print(f"Fixer.io API call failed: {data.get('error', 'Unknown error')}")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching currency rates from Fixer.io: {e}")
    
    # Placeholder for categorization logic
    if "amazon" in (normalized_expense.vendor_name or "").lower():
        normalized_expense.category = "Online Shopping"
    elif "starbucks" in (normalized_expense.vendor_name or "").lower():
        normalized_expense.category = "Food & Drink"
    else:
        normalized_expense.category = "Uncategorized"

    return normalized_expense
