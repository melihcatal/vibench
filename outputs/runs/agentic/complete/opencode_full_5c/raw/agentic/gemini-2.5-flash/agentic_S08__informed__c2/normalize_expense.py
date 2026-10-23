import json
from typing import Dict, Any
from document_models import (
    ExtractedInvoice,
    ExtractedReceipt,
    NormalizedExpense,
    LineItem,
)
from document_client import get_gemini_client


def normalize_expense(extracted_data: Any, document_type: str) -> NormalizedExpense:
    """
    Normalizes extracted expense fields into a standard JSON schema using Google Gemini API
    for intelligent field mapping and enrichment.
    """
    client = get_gemini_client()

    # Create a prompt for Gemini to normalize the data
    schema = NormalizedExpense.__annotations__
    line_item_schema = LineItem.__annotations__

    prompt_parts = [
        f"You are an AI assistant that normalizes extracted document fields into a standard JSON schema. "
        f"Given the extracted data and the target schema, map the fields as accurately as possible. "
        f"If a field from the extracted data doesn't directly map, try to infer it if possible or leave it null. "
        f"The document type is '{document_type}'.\n\n",
        f"Target NormalizedExpense Schema:\n{json.dumps({k: str(v) for k, v in schema.items()}, indent=2)}\n\n",
        f"Target LineItem Schema:\n{json.dumps({k: str(v) for k, v in line_item_schema.items()}, indent=2)}\n\n",
        f"Extracted Data:\n{json.dumps(extracted_data.__dict__, indent=2)}\n\n",
        "Normalize the extracted data into the NormalizedExpense JSON schema. Respond with only the JSON object.",
    ]

    response = client.generate_content(prompt_parts)

    try:
        normalized_json = json.loads(response.text.strip())
        # Convert line items from dict to LineItem objects if present
        if "line_items" in normalized_json and isinstance(
            normalized_json["line_items"], list
        ):
            normalized_json["line_items"] = [
                LineItem(**item) for item in normalized_json["line_items"]
            ]

        # Pop document_type if it's already in normalized_json to avoid duplicate argument in constructor
        if "document_type" in normalized_json:
            del normalized_json["document_type"]

        normalized_expense = NormalizedExpense(
            document_type=document_type, **normalized_json
        )
    except json.JSONDecodeError:
        print(f"Error decoding JSON from Gemini: {response.text}")
        # Fallback to a simpler, direct mapping if Gemini fails or returns malformed JSON
        normalized_expense = NormalizedExpense(document_type=document_type)
        if isinstance(extracted_data, ExtractedInvoice):
            normalized_expense.vendor_name = extracted_data.vendor_name
            normalized_expense.transaction_date = extracted_data.invoice_date
            normalized_expense.total_amount = extracted_data.total_amount
            normalized_expense.currency = extracted_data.currency
            normalized_expense.line_items = extracted_data.line_items
            normalized_expense.vendor_notes = (
                extracted_data.raw_text
            )  # Using raw_text as notes for now
        elif isinstance(extracted_data, ExtractedReceipt):
            normalized_expense.vendor_name = extracted_data.merchant_name
            normalized_expense.transaction_date = extracted_data.transaction_date
            normalized_expense.total_amount = extracted_data.total_amount
            normalized_expense.currency = extracted_data.currency
            normalized_expense.line_items = extracted_data.items
            normalized_expense.tax_amount = extracted_data.tax_amount
            normalized_expense.vendor_notes = (
                extracted_data.raw_text
            )  # Using raw_text as notes for now

    return normalized_expense
