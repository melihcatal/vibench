import json
import google.generativeai as genai
import os


def normalize_expense(extracted_data: dict) -> dict:
    """
    Normalizes extracted expense fields into a standard JSON schema using Google Gemini.
    """
    # Configure the generative AI model
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel(
        "gemini-pro"
    )  # Using a suitable model for text generation

    # Define a target schema for normalization
    target_schema = {
        "type": "object",
        "properties": {
            "transaction_type": {"type": "string", "enum": ["invoice", "receipt"]},
            "vendor_name": {"type": "string"},
            "transaction_date": {"type": "string", "format": "date"},
            "total_amount": {"type": "number"},
            "currency": {"type": "string"},
            "line_items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "description": {"type": "string"},
                        "quantity": {"type": "number"},
                        "unit_price": {"type": "number"},
                        "amount": {"type": "number"},
                    },
                    "required": ["description", "amount"],
                },
            },
            "tax_amount": {"type": "number"},
            "notes": {"type": "string"},
        },
        "required": [
            "transaction_type",
            "vendor_name",
            "transaction_date",
            "total_amount",
            "currency",
        ],
    }

    # Construct the prompt for Gemini
    prompt = f"""Normalize the following extracted document data into the provided JSON schema. 
    Infer 'transaction_type' as 'invoice' or 'receipt' based on the presence of 'invoice_date' or 'receipt_date', and other relevant fields. 
    Assume currency is USD if not explicitly present. Output only the JSON.

    Extracted Data: {json.dumps(extracted_data, indent=2)}

    Target JSON Schema: {json.dumps(target_schema, indent=2)}

    Normalized JSON:
    """

    try:
        response = model.generate_content(prompt)
        normalized_json_str = response.text.strip()
        # Clean up any potential markdown formatting from Gemini's response
        if normalized_json_str.startswith("```json") and normalized_json_str.endswith(
            "```"
        ):
            normalized_json_str = normalized_json_str[7:-3].strip()
        elif normalized_json_str.startswith("```") and normalized_json_str.endswith(
            "```"
        ):
            normalized_json_str = normalized_json_str[3:-3].strip()

        normalized_data = json.loads(normalized_json_str)
        return normalized_data
    except Exception as e:
        print(f"Error normalizing data with Gemini: {e}")
        return {"error": str(e), "original_data": extracted_data}
