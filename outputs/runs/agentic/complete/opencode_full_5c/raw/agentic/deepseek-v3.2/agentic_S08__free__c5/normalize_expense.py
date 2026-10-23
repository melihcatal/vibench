import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from document_models import ExpenseRecord, NormalizedExpense


def normalize_expense(
    extracted_data: Dict[str, Any], source_type: str = "invoice"
) -> Dict[str, Any]:
    """
    Normalize extracted expense fields into a standard JSON schema using OpenAI's GPT for field normalization.
    """
    import openai

    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Prepare the prompt for normalization
    prompt = f"""
    Normalize the following {source_type} data into a standardized expense schema:
    
    Raw data: {json.dumps(extracted_data, indent=2)}
    
    Please provide a normalized JSON object with these fields:
    - vendor_name (string)
    - transaction_date (ISO 8601 date string)
    - total_amount (float)
    - currency (string, default to USD)
    - line_items (array of objects with description, quantity, unit_price, amount)
    - tax_amount (float, optional)
    - category (string, inferred from vendor or items)
    
    Return ONLY the JSON object, no other text.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a data normalization assistant. Always return valid JSON.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.1,
            max_tokens=500,
        )

        normalized_json = response.choices[0].message.content.strip()

        # Parse the JSON response
        normalized_data = json.loads(normalized_json)

        # Add metadata
        normalized_data["source_type"] = source_type
        normalized_data["normalized_at"] = datetime.utcnow().isoformat()
        normalized_data["extraction_source"] = (
            "document_ai" if source_type == "receipt" else "form_recognizer"
        )

        return normalized_data

    except Exception as e:
        # Fallback to manual normalization if OpenAI fails
        return manual_normalize_expense(extracted_data, source_type)


def manual_normalize_expense(
    extracted_data: Dict[str, Any], source_type: str
) -> Dict[str, Any]:
    """Manual normalization fallback"""
    normalized = {
        "vendor_name": extracted_data.get("vendor") or extracted_data.get("merchant"),
        "transaction_date": None,
        "total_amount": None,
        "currency": "USD",
        "line_items": [],
        "tax_amount": extracted_data.get("tax"),
        "category": "uncategorized",
        "source_type": source_type,
        "normalized_at": datetime.utcnow().isoformat(),
        "extraction_source": "manual_fallback",
    }

    # Parse date
    date_value = extracted_data.get("date")
    if date_value:
        if isinstance(date_value, str):
            normalized["transaction_date"] = date_value
        elif hasattr(date_value, "isoformat"):
            normalized["transaction_date"] = date_value.isoformat()

    # Parse total
    total_value = extracted_data.get("total")
    if total_value:
        if isinstance(total_value, (int, float)):
            normalized["total_amount"] = float(total_value)
        elif isinstance(total_value, str):
            try:
                # Remove currency symbols and commas
                cleaned = total_value.replace("$", "").replace(",", "").strip()
                normalized["total_amount"] = float(cleaned)
            except:
                pass

    # Normalize line items
    items = extracted_data.get("line_items") or extracted_data.get("items") or []
    for item in items:
        normalized_item = {
            "description": item.get("description", ""),
            "quantity": float(item.get("quantity", 1)),
            "unit_price": float(item.get("unit_price", 0)),
            "amount": float(item.get("amount", 0)),
        }
        normalized["line_items"].append(normalized_item)

    return normalized


if __name__ == "__main__":
    # Example usage
    sample_data = {
        "vendor": "ABC Supplies",
        "date": "2024-01-15",
        "total": 1250.75,
        "line_items": [
            {
                "description": "Office chairs",
                "quantity": 5,
                "unit_price": 200,
                "amount": 1000,
            },
            {
                "description": "Desk lamps",
                "quantity": 3,
                "unit_price": 83.58,
                "amount": 250.75,
            },
        ],
    }

    result = normalize_expense(sample_data, "invoice")
    print(json.dumps(result, indent=2))
