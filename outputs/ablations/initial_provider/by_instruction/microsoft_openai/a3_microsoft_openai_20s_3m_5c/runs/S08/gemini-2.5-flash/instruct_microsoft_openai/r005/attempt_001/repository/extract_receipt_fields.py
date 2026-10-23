import json
from typing import Optional
from document_client import get_openai_client, call_openai_chat_model
from document_models import ReceiptFields, LineItem

def extract_receipt_fields(receipt_content: str, model_deployment_name: str = "gpt-4o") -> Optional[ReceiptFields]:
    """
    Extracts merchant, tax, total, and items from a receipt using Azure OpenAI.
    """
    client = get_openai_client()

    prompt = f"""
    Extract the following fields from the receipt text provided below in JSON format:
    - Merchant Name (merchant_name)
    - Transaction Date (transaction_date) in YYYY-MM-DD format
    - Total Amount (total_amount)
    - Tax Amount (tax_amount)
    - Items (items) as a list of objects, each with 'description', 'quantity', 'unit_price', and 'total'.
    If a field is not found, return null for its value.

    Receipt Text:
    """
    {receipt_content}
    """

    Example JSON format:
    {{
        "merchant_name": "Coffee Shop",
        "transaction_date": "2023-10-26",
        "total_amount": 5.75,
        "tax_amount": 0.25,
        "items": [
            {{
                "description": "Coffee",
                "quantity": 1.0,
                "unit_price": 3.50,
                "total": 3.50
            }},
            {{
                "description": "Pastry",
                "quantity": 1.0,
                "unit_price": 2.00,
                "total": 2.00
            }}
        ]
    }}
    """

    try:
        response_content = call_openai_chat_model(client, model_deployment_name, prompt)
        extracted_data = json.loads(response_content)

        line_items = [
            LineItem(**item)
            for item in extracted_data.get("items", [])
        ]

        return ReceiptFields(
            merchant_name=extracted_data.get("merchant_name"),
            transaction_date=extracted_data.get("transaction_date"),
            total_amount=extracted_data.get("total_amount"),
            tax_amount=extracted_data.get("tax_amount"),
            items=line_items
        )
    except Exception as e:
        print(f"Error extracting receipt fields: {e}")
        return None
