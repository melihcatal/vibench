import uuid
import datetime

def normalize_expense_fields(extracted_data: dict) -> dict:
    """
    Normalizes extracted expense fields into a standard JSON schema.

    This function hypothetically integrates with Google Cloud Document AI
    for structured document extraction and then normalizes the output.
    """
    normalized_data = {
        "provider": "Google Cloud Document AI (hypothetical)",
        "expenseId": str(uuid.uuid4()),
        "date": extracted_data.get("transaction_date"),
        "vendor": {
            "name": extracted_data.get("merchant_name")
        },
        "total": {
            "amount": float(extracted_data.get("total_amount", 0.0)),
            "currency": extracted_data.get("currency", "USD")
        },
        "tax": {
            "amount": float(extracted_data.get("tax_amount", 0.0)),
            "currency": extracted_data.get("currency", "USD")
        },
        "lineItems": []
    }

    for item in extracted_data.get("items", []):
        normalized_data["lineItems"].append({
            "description": item.get("description"),
            "amount": float(item.get("amount", 0.0)),
            "currency": extracted_data.get("currency", "USD")
        })

    return normalized_data
