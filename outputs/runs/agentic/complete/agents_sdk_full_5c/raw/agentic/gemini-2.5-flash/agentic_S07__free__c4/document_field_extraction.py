import os
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part, Content
from typing import Dict, Any
import json

def extract_structured_fields(document_text: str, project_id: str, location: str = "us-central1", schema: Dict[str, str] = None) -> Dict[str, Any]:
    """Extracts structured fields from OCR-normalized document text using Google Cloud Vertex AI GenerativeModel.
    The schema should be a dictionary where keys are field names and values are descriptions of the expected content.
    """
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel("gemini-pro") # Using a general purpose Gemini model

    if schema is None:
        # Default schema for a generic invoice-like document
        schema = {
            "invoice_number": "The unique identifier for the invoice, e.g., INV-2023-001",
            "total_amount": "The total amount due, including currency, e.g., $123.45",
            "date": "The date of the invoice, e.g., 2023-10-26",
            "vendor_name": "The name of the vendor or supplier",
            "customer_name": "The name of the customer or recipient",
        }

    schema_str = json.dumps(schema, indent=2)

    prompt = f"""
    You are an expert at extracting information from documents. Read the following document text and extract the specified fields.
    Return the extracted information as a JSON object matching the provided schema. If a field is not found, use null.

    Document Text:
    '''
    {document_text}
    '''

    Extraction Schema:
    '''
    {schema_str}
    '''

    Extracted JSON:
    """

    contents = [Part.from_text(prompt)]

    try:
        response = model.generate_content(contents, generation_config={"temperature": 0.0})
        # Assuming the model returns valid JSON in text form
        if response.text:
            return json.loads(response.text)
    except Exception as e:
        print(f"Error during field extraction: {e}")
        return {"error": str(e)}
    return {}

if __name__ == '__main__':
    _project_id = os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id") # Replace with your project ID
    _location = "us-central1"

    _sample_document_text = """
    INVOICE
    Invoice No: 12345
    Date: 2023-11-15
    Total Due: $500.75
    Vendor: Example Corp
    Customer: Acme Inc.
    """

    _extracted_fields = extract_structured_fields(_sample_document_text, _project_id, _location)
    print(f"Extracted Fields: {json.dumps(_extracted_fields, indent=2)}")

    _custom_schema = {
        "order_id": "The identifier for the order",
        "shipping_address": "The full shipping address",
        "delivery_date": "The expected delivery date",
    }
    _another_document_text = """
    Order Confirmation #XYZ-987
    Ship to: 123 Main St, Anytown, CA 90210
    Expected by: December 1, 2023
    """
    _extracted_fields_custom = extract_structured_fields(_another_document_text, _project_id, _location, _custom_schema)
    print(f"\nExtracted Fields with Custom Schema: {json.dumps(_extracted_fields_custom, indent=2)}")
