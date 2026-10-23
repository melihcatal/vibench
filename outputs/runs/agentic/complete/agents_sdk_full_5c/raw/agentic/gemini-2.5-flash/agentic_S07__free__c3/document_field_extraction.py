import google.generativeai as genai
import os
import json
from typing import Dict, Any

def extract_structured_fields(document_text: str, schema: Dict[str, str]) -> Dict[str, Any]:
    """Extracts structured fields from OCR-normalized document text using Google Generative AI (Gemini Pro).

    Args:
        document_text: The full text content of the document.
        schema: A dictionary defining the desired output structure, where keys are field names
                and values are descriptions/types (e.g., {"invoice_number": "string", "total_amount": "float"}).

    Returns:
        A dictionary containing the extracted fields and their values.
    """
    # Ensure GOOGLE_API_KEY is set as an environment variable or configured
    # genai.configure(api_key="YOUR_API_KEY") # Uncomment and set your API key if not using env var

    model = genai.GenerativeModel('gemini-pro')

    schema_str = json.dumps(schema)
    prompt = f"""Given the following document text, extract the information according to the provided JSON schema.
    If a field is not found, use null.

    Document Text:
    '''
    {document_text}
    '''

    JSON Schema for extraction (field_name: description/type):
    {schema_str}

    Provide the extracted information as a JSON object, matching the schema keys.
    """

    response = model.generate_content(prompt)
    
    # Attempt to parse the response text as JSON
    try:
        # The model might return markdown code block, so try to extract JSON from it
        response_text = response.text.strip()
        if response_text.startswith('```json') and response_text.endswith('```'):
            json_str = response_text[len('```json'):-len('```')].strip()
            extracted_data = json.loads(json_str)
        else:
            extracted_data = json.loads(response_text)
    except json.JSONDecodeError:
        print(f"Warning: Could not decode JSON from model response: {response.text}")
        return {"error": "Failed to parse model output as JSON", "raw_output": response.text}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {"error": f"An unexpected error occurred: {e}", "raw_output": response.text}

    return extracted_data

if __name__ == '__main__':
    # Example usage (requires GOOGLE_API_KEY environment variable to be set)
    # os.environ["GOOGLE_API_KEY"] = "YOUR_API_KEY"
    # sample_document_text = "Invoice #12345. Date: 2023-10-27. Amount Due: $150.75. Customer: John Doe."
    # extraction_schema = {
    #     "invoice_number": "string, the unique identifier of the invoice",
    #     "invoice_date": "string, the date of the invoice in YYYY-MM-DD format",
    #     "total_amount": "float, the total amount due",
    #     "customer_name": "string, the name of the customer"
    # }
    # extracted_fields = extract_structured_fields(sample_document_text, extraction_schema)
    # print(f"Document Text: '{sample_document_text}'")
    # print(f"Extracted Fields: {json.dumps(extracted_fields, indent=2)}")

    # sample_document_text_missing_field = "Invoice #987. Date: 2023-11-01. Total: $25.00."
    # extracted_fields_missing = extract_structured_fields(sample_document_text_missing_field, extraction_schema)
    # print(f"\nDocument Text: '{sample_document_text_missing_field}'")
    # print(f"Extracted Fields (missing customer): {json.dumps(extracted_fields_missing, indent=2)}")
    pass
