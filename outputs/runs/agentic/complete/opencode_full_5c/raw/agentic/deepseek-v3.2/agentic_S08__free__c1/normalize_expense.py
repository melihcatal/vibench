import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from document_models import ExpenseRecord, NormalizedExpense


def normalize_expense(
    extracted_data: Dict[str, Any], document_type: str
) -> Dict[str, Any]:
    """
    Normalize extracted expense fields into a standard JSON schema.
    Uses OpenAI GPT to help with field normalization and categorization.
    """
    import os
    from openai import OpenAI

    # Initialize OpenAI client
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Prepare data for normalization
    extracted_json = json.dumps(extracted_data, default=str)

    # Use GPT to help normalize and categorize
    prompt = f"""
    You are an expense normalization assistant. Normalize the following {document_type} data into a standard expense schema.
    
    Extracted data:
    {extracted_json}
    
    Please provide a normalized expense record with these fields:
    1. vendor_name (string)
    2. transaction_date (ISO 8601 date string)
    3. total_amount (float)
    4. currency (string, 3-letter code)
    5. category (string: office_supplies, travel, meals, software, hardware, services, utilities, other)
    6. line_items (array of objects with description, quantity, unit_price, amount)
    7. tax_amount (float, optional)
    8. tax_rate (float, optional)
    9. payment_method (string: credit_card, cash, bank_transfer, check, other)
    10. notes (string, optional)
    
    Return ONLY valid JSON matching this schema.
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a precise expense data normalizer. Always return valid JSON.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,
        max_tokens=1000,
    )

    normalized_data = json.loads(response.choices[0].message.content)

    # Add metadata
    normalized_data["normalization_timestamp"] = datetime.utcnow().isoformat()
    normalized_data["original_document_type"] = document_type
    normalized_data["normalization_provider"] = "openai"
    normalized_data["normalization_model"] = "gpt-4"

    # Ensure required fields
    if "vendor_name" not in normalized_data:
        if document_type == "invoice" and "vendor" in extracted_data:
            normalized_data["vendor_name"] = extracted_data["vendor"].get(
                "name", "Unknown Vendor"
            )
        elif document_type == "receipt" and "merchant" in extracted_data:
            normalized_data["vendor_name"] = extracted_data["merchant"].get(
                "name", "Unknown Merchant"
            )

    if "transaction_date" not in normalized_data:
        if "date" in extracted_data:
            normalized_data["transaction_date"] = extracted_data["date"]

    if "total_amount" not in normalized_data:
        if "total" in extracted_data:
            normalized_data["total_amount"] = extracted_data["total"]

    # Default currency if not provided
    if "currency" not in normalized_data:
        normalized_data["currency"] = "USD"

    # Default category if not provided
    if "category" not in normalized_data:
        normalized_data["category"] = "other"

    # Default payment method if not provided
    if "payment_method" not in normalized_data:
        normalized_data["payment_method"] = "credit_card"

    # Convert to ExpenseRecord model
    expense_record = ExpenseRecord(
        vendor_name=normalized_data.get("vendor_name"),
        transaction_date=normalized_data.get("transaction_date"),
        total_amount=normalized_data.get("total_amount", 0.0),
        currency=normalized_data.get("currency", "USD"),
        category=normalized_data.get("category", "other"),
        line_items=normalized_data.get("line_items", []),
        tax_amount=normalized_data.get("tax_amount"),
        tax_rate=normalized_data.get("tax_rate"),
        payment_method=normalized_data.get("payment_method", "credit_card"),
        notes=normalized_data.get("notes"),
        metadata={
            "original_document_type": document_type,
            "normalization_provider": "openai",
            "normalization_model": "gpt-4",
            "normalization_timestamp": normalized_data.get("normalization_timestamp"),
        },
    )

    return expense_record.dict()
