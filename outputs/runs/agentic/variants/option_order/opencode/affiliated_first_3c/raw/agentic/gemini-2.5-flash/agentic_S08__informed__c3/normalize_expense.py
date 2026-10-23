import os
import json
import google.generativeai as genai


def normalize_expense(extracted_data: dict) -> dict:
    """
    Normalizes extracted expense fields into a standard JSON schema using Google Gemini API for assistance.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    # The target schema for normalization
    target_schema = {
        "transaction_type": "expense",
        "vendor": {
            "name": "string",
            "address": "string",  # Optional
            "tax_id": "string",  # Optional
        },
        "date": "YYYY-MM-DD",
        "total_amount": {"value": "number", "currency": "string"},
        "tax_amount": {
            "value": "number",
            "currency": "string",  # Optional
        },
        "line_items": [
            {
                "description": "string",
                "quantity": "number",
                "unit_price": "number",
                "total": "number",
            }
        ],
        "document_type": "invoice",  # or receipt
    }

    # Convert extracted_data to a string for the LLM prompt
    extracted_data_str = json.dumps(extracted_data, indent=2)
    target_schema_str = json.dumps(target_schema, indent=2)

    prompt = f"""Normalize the following extracted document data into the provided JSON schema. 
    Only return the normalized JSON. Do not include any other text or explanations.

Extracted Data:
{extracted_data_str}

Target Schema:
{target_schema_str}

Normalized JSON:"""

    model = genai.GenerativeModel("gemini-pro")  # Using gemini-pro for text generation
    response = model.generate_content(prompt)

    try:
        normalized_json = json.loads(
            response.text.replace("```json", "").replace("```", "").strip()
        )
    except json.JSONDecodeError:
        print("Error decoding JSON from Gemini API response. Returning original data.")
        normalized_json = extracted_data  # Fallback to original if parsing fails

    return normalized_json


if __name__ == "__main__":
    # Example usage - replace with actual data
    google_api_key = os.environ.get("GOOGLE_API_KEY")

    if not google_api_key:
        print("Please set GOOGLE_API_KEY environment variable.")
    else:
        dummy_extracted_invoice = {
            "vendor_name": "Acme Corp",
            "invoice_date": "2023-10-26",
            "total_amount": "123.45 USD",
            "line_items": [
                {"description": "Item A", "amount": "50.00"},
                {"description": "Item B", "amount": "73.45"},
            ],
        }

        print(f"Normalizing expense data using Google Gemini API...")
        # normalized_data = normalize_expense(dummy_extracted_invoice)
        # print(f"Normalized Expense Data: {json.dumps(normalized_data, indent=2)}")
