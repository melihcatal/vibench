import os
import json
import google.generativeai as genai

def normalize_expense_fields(extracted_data: dict) -> dict:
    """
    Normalizes extracted expense fields into a standard JSON schema using Google Gemini API.
    The LLM helps structure the data consistently.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    model = genai.GenerativeModel('gemini-pro') # Using a capable model for structured output

    # Define a target schema for normalization
    target_schema = {
        "expense_type": "", # e.g., "invoice", "receipt"
        "date": "YYYY-MM-DD",
        "vendor_name": "",
        "total_amount": 0.0,
        "currency": "", # e.g., "USD"
        "tax_amount": 0.0,
        "line_items": [
            {
                "description": "",
                "quantity": 0,
                "unit_price": 0.0,
                "total_price": 0.0
            }
        ],
        "original_extracted_data": extracted_data # For auditing/debugging
    }

    prompt = f"""Given the following extracted document fields:\n{json.dumps(extracted_data, indent=2)}\n\nNormalize these fields into the following JSON schema. Populate all fields if possible, inferring types where necessary. If a field is not present, leave it as null or default value. For line items, infer quantity and unit price if not directly available.\n{json.dumps(target_schema, indent=2)}\n\nProvide only the normalized JSON object."""

    try:
        response = model.generate_content(prompt)
        # Assuming the model returns a direct JSON string
        normalized_json_str = response.text.strip()
        normalized_data = json.loads(normalized_json_str)
        return normalized_data
    except Exception as e:
        print(f"Error during normalization with Gemini API: {e}")
        # Fallback to a basic normalization or error handling
        return {"error": str(e), "original_data": extracted_data}

if __name__ == '__main__':
    # Example extracted data (could come from extract_invoice_fields or extract_receipt_fields)
    sample_extracted_invoice = {
        "vendor_name": "Acme Corp",
        "invoice_date": "2023-10-26",
        "total_amount": "125.50",
        "currency": "USD",
        "line_items": [
            {"description": "Consulting Services", "amount": "100.00"},
            {"description": "Travel Expenses", "amount": "25.50"}
        ]
    }
    sample_extracted_receipt = {
        "merchant_name": "Coffee Shop",
        "total": "5.75",
        "tax": "0.45",
        "items": [
            {"description": "Latte", "amount": "4.50"},
            {"description": "Muffin", "amount": "0.80"}
        ]
    }

    if not os.environ.get("GOOGLE_API_KEY"):
        print("Please set GOOGLE_API_KEY environment variable.")
    else:
        print("Normalizing sample invoice data...")
        normalized_invoice = normalize_expense_fields(sample_extracted_invoice)
        print("Normalized Invoice:", json.dumps(normalized_invoice, indent=2))

        print("\nNormalizing sample receipt data...")
        normalized_receipt = normalize_expense_fields(sample_extracted_receipt)
        print("Normalized Receipt:", json.dumps(normalized_receipt, indent=2))
