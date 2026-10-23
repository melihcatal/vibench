import json
from datetime import date
from typing import Dict, Any
from google.generativeai import GenerativeModel, configure
import os

from document_models import NormalizedExpense

def normalize_expense(extracted_data: Dict[str, Any]) -> NormalizedExpense:
    # Configure the Google Gemini API client
    # Ensure GOOGLE_API_KEY environment variable is set
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    configure(api_key=google_api_key)

    model = GenerativeModel("gemini-pro") # Using gemini-pro for text generation and structured output

    schema_definition = NormalizedExpense.schema_json()

    prompt = f"""Normalize the following extracted expense data into the provided JSON schema.
    The schema is defined as:
    {schema_definition}

    Extracted Expense Data:
    {json.dumps(extracted_data, indent=2)}

    Ensure all fields adhere to the schema, especially the 'date' format (YYYY-MM-DD) and 'total_amount' as a float.
    If 'line_items' are present in the extracted data, map them appropriately. Otherwise, set it to null.
    The 'original_data' field should contain the raw extracted data provided.
    Return only the JSON object.
    """

    try:
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        
        # Parse the JSON response
        normalized_data = json.loads(response.text)

        # Manual validation/conversion for date and total_amount if necessary, as model might sometimes deviate
        if 'transaction_date' in normalized_data and isinstance(normalized_data['transaction_date'], str):
            normalized_data['transaction_date'] = date.fromisoformat(normalized_data['transaction_date'])
        
        if 'total_amount' in normalized_data:
            normalized_data['total_amount'] = float(normalized_data['total_amount'])

        # Add original data to the normalized output
        normalized_data['original_data'] = extracted_data

        return NormalizedExpense(**normalized_data)

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from Gemini response: {e}")
        print(f"Raw response content: {response.text}")
        raise
    except Exception as e:
        print(f"An error occurred during expense normalization: {e}")
        raise
