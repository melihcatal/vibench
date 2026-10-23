import google.generativeai as genai
import json

def document_field_extraction(payload, config=None):
    config = config or {}
    genai.configure(api_key=config["gemini_api_key"])
    model = genai.GenerativeModel('gemini-pro')

    document_text = payload["text"]
    
    # Example of a prompt for extracting structured fields. 
    # The actual fields to extract would be defined by the user/task.
    prompt = f"""Extract the following fields from the document text as a JSON object. If a field is not found, use null.
Expected fields: InvoiceNumber, TotalAmount, IssueDate, VendorName, CustomerName.

Document Text:
{document_text}

JSON Output:"""

    response = model.generate_content(prompt)
    
    try:
        extracted_fields = json.loads(response.text.strip())
    except json.JSONDecodeError:
        extracted_fields = {"error": "Could not parse JSON from model response", "raw_response": response.text}

    return {"extracted_fields": extracted_fields, "original_text": document_text}
