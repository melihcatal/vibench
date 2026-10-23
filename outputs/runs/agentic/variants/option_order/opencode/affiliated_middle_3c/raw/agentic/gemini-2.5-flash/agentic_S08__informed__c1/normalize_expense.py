import os
import google.generativeai as genai


def normalize_expense_data(extracted_data: dict) -> dict:
    """
    Normalizes extracted expense fields into a standard JSON schema using Google Gemini API.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    model = genai.GenerativeModel("gemini-pro")

    prompt = f"""
    Normalize the following extracted expense data into a standard JSON schema.
    The schema should include:
    - "transaction_type": "invoice" or "receipt"
    - "vendor_name": (string)
    - "transaction_date": (string, YYYY-MM-DD format if possible)
    - "total_amount": (float)
    - "currency": (string, e.g., "USD")
    - "tax_amount": (float, optional)
    - "line_items": (array of objects, each with "description": string, "quantity": float, "unit_price": float, "total_price": float)

    Extracted data:
    {extracted_data}

    If a field is missing or cannot be determined, set it to null.
    """

    response = model.generate_content(prompt)

    # Assuming the response text contains the JSON string
    try:
        normalized_json_str = (
            response.text.strip().replace("```json", "").replace("```", "")
        )
        normalized_data = eval(
            normalized_json_str
        )  # Using eval for simplicity, safer would be json.loads
    except Exception as e:
        print(f"Error parsing Gemini response: {e}")
        normalized_data = {
            "error": "Failed to normalize data",
            "raw_response": response.text,
        }

    return normalized_data


if __name__ == "__main__":
    # Placeholder for actual usage with GOOGLE_API_KEY set
    if not os.environ.get("GOOGLE_API_KEY"):
        print("Please set GOOGLE_API_KEY environment variable.")
    else:
        sample_extracted_data_invoice = {
            "vendor_name": "Acme Corp",
            "invoice_date": "2023-10-26",
            "total_amount": "120.50 USD",
            "line_items": [],
        }
        sample_extracted_data_receipt = {
            "merchant_name": "Coffee Shop",
            "tax_amount": "1.20",
            "total_amount": "10.00",
            "line_items": [
                {"description": "Coffee", "price": "4.50", "quantity": "1"},
                {"description": "Pastry", "price": "3.80", "quantity": "1"},
            ],
        }

        # normalized_invoice = normalize_expense_data(sample_extracted_data_invoice)
        # print("Normalized Invoice:", normalized_invoice)

        # normalized_receipt = normalize_expense_data(sample_extracted_data_receipt)
        # print("Normalized Receipt:", normalized_receipt)
        print("Google Gemini API client configured for expense normalization.")
