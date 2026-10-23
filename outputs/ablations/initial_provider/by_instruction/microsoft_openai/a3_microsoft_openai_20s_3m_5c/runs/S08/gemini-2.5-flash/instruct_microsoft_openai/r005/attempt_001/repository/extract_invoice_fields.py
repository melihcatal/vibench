import json
from typing import Optional
from document_client import get_openai_client, call_openai_chat_model
from document_models import InvoiceFields, LineItem

def extract_invoice_fields(invoice_content: str, model_deployment_name: str = "gpt-4o") -> Optional[InvoiceFields]:
    """
    Extracts vendor, date, total, and line-item fields from an invoice using Azure OpenAI.
    """
    client = get_openai_client()

    prompt = f"""
    Extract the following fields from the invoice text provided below in JSON format:
    - Vendor Name (vendor_name)
    - Invoice Date (invoice_date) in YYYY-MM-DD format
    - Total Amount (total_amount)
    - Line Items (line_items) as a list of objects, each with 'description', 'quantity', 'unit_price', and 'total'.
    If a field is not found, return null for its value.

    Invoice Text:
    """
    {invoice_content}
    """

    Example JSON format:
    {{
        "vendor_name": "Example Corp",
        "invoice_date": "2023-10-26",
        "total_amount": 123.45,
        "line_items": [
            {{
                "description": "Item 1",
                "quantity": 1.0,
                "unit_price": 100.00,
                "total": 100.00
            }},
            {{
                "description": "Item 2",
                "quantity": 2.0,
                "unit_price": 10.00,
                "total": 20.00
            }}
        ]
    }}
    """

    try:
        response_content = call_openai_chat_model(client, model_deployment_name, prompt)
        extracted_data = json.loads(response_content)

        line_items = [
            LineItem(**item)
            for item in extracted_data.get("line_items", [])
        ]

        return InvoiceFields(
            vendor_name=extracted_data.get("vendor_name"),
            invoice_date=extracted_data.get("invoice_date"),
            total_amount=extracted_data.get("total_amount"),
            line_items=line_items
        )
    except Exception as e:
        print(f"Error extracting invoice fields: {e}")
        return None
