import json
from typing import Dict, Any, List, Optional
from document_models import NormalizedExpense, LineItem
from document_client import get_gemini_model


def normalize_expense(extracted_data: Dict[str, Any]) -> NormalizedExpense:
    model = get_gemini_model(model_name="gemini-pro")

    prompt_template = """
    You are an AI assistant tasked with normalizing expense data into a standard JSON schema.
    The input will be a dictionary of extracted fields from an invoice or receipt.
    Your task is to convert this data into the following JSON format:

    {{
        "vendor_name": <string, name of the vendor/merchant>,
        "transaction_date": <string, date of the transaction in YYYY-MM-DD format>,
        "total_amount": <float, total amount of the expense>,
        "currency": <string, currency code, e.g., "USD">,
        "category": <string, inferred category of the expense, e.g., "Food", "Travel", "Office Supplies">,
        "description": <string, a brief overall description of the expense>,
        "line_items": [
            {{
                "description": <string, description of the item>,
                "quantity": <float, optional>,
                "unit_price": <float, optional>,
                "amount": <float, optional>
            }}
        ]
    }}

    If a field is not available or cannot be reasonably inferred, omit it or set to null.
    Ensure the output is valid JSON.

    Here is the extracted data:
    {}
    """

    prompt = prompt_template.format(json.dumps(extracted_data, indent=2))

    response = model.generate_content(prompt)

    normalized_json_str = response.text.strip()
    # Attempt to extract JSON from potential markdown code block
    if normalized_json_str.startswith("```json") and normalized_json_str.endswith(
        "```"
    ):
        normalized_json_str = normalized_json_str[len("```json") : -len("```")].strip()
    elif normalized_json_str.startswith("```") and normalized_json_str.endswith("```"):
        normalized_json_str = normalized_json_str[len("```") : -len("```")].strip()

    try:
        normalized_data = json.loads(normalized_json_str)
    except json.JSONDecodeError:
        print(f"Error decoding JSON from Gemini: {normalized_json_str}")
        return NormalizedExpense(
            vendor_name=None,
            transaction_date=None,
            total_amount=None,
            currency=None,
            category=None,
            description=None,
        )

    line_items: List[LineItem] = []
    for item_data in normalized_data.get("line_items", []) or []:
        line_items.append(
            LineItem(
                description=item_data.get("description", ""),
                quantity=item_data.get("quantity"),
                unit_price=item_data.get("unit_price"),
                amount=item_data.get("amount"),
            )
        )

    return NormalizedExpense(
        vendor_name=normalized_data.get("vendor_name"),
        transaction_date=normalized_data.get("transaction_date"),
        total_amount=normalized_data.get("total_amount"),
        currency=normalized_data.get("currency"),
        category=normalized_data.get("category"),
        description=normalized_data.get("description"),
        line_items=line_items,
    )
