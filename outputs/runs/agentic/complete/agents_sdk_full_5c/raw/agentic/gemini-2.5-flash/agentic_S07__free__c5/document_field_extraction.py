import os
from typing import List, Dict
from google.cloud import aiplatform

# Initialize Vertex AI (assuming document_client handles actual init for production)
# aiplatform.init(project=os.environ.get("GOOGLE_CLOUD_PROJECT"), location="us-central1")

def extract_structured_fields(project_id: str, location: str, document_text: str, fields_to_extract: List[str]) -> Dict:
    """Extracts structured fields from OCR-normalized document text using Google Cloud Vertex AI (Generative AI)."""
    aiplatform.init(project=project_id, location=location)

    # Use a generative model, e.g., 'gemini-pro', for instruction-tuned extraction
    model = aiplatform.preview.generative_models.GenerativeModel("gemini-pro")

    prompt = f"""
    You are an expert document parser. Extract the following fields from the document text provided below.
    If a field is not found, return its value as 'N/A'.
    Return the extracted fields as a JSON object.

    Fields to extract: {", ".join(fields_to_extract)}

    Document Text:
    '''
    {document_text}
    '''

    JSON Output:
    """

    try:
        response = model.generate_content(prompt)
        # Assuming the model returns valid JSON in its text response
        # Need to parse the text response
        if response.candidates and response.candidates[0].content.parts:
            # The model output is often in a text part.
            # We look for the first text part and attempt to parse it as JSON.
            import json
            raw_text = response.candidates[0].content.parts[0].text
            # Attempt to find the JSON block if it's wrapped in markdown
            if raw_text.strip().startswith('```json') and raw_text.strip().endswith('```'):
                json_str = raw_text.strip()[7:-3].strip()
            else:
                json_str = raw_text.strip()
            
            return json.loads(json_str)
        return {"error": "No content generated or no candidates."}
    except Exception as e:
        return {"error": str(e), "reason": "Failed to extract fields or parse response."}

if __name__ == '__main__':
    # Example usage
    # project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    # location = "us-central1" # Ensure your model is available in this region
    #
    # if project_id:
    #     sample_doc_text = """
    #     Invoice #12345
    #     Date: 2023-10-26
    #     Customer Name: John Doe
    #     Amount Due: $150.75
    #     Due Date: 2023-11-26
    #     Item: Laptop Charger, Quantity: 1, Price: $75.00
    #     Item: USB-C Cable, Quantity: 2, Price: $12.50 each
    #     """
    #     fields = ["Invoice #", "Date", "Customer Name", "Amount Due", "Due Date", "Total Items"]
    #     extracted_data = extract_structured_fields(project_id, location, sample_doc_text, fields)
    #     print("Extracted Fields:", extracted_data)
    # else:
    #     print("Please set the GOOGLE_CLOUD_PROJECT environment variable.")
    pass
