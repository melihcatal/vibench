import os
import google.generativeai as genai

def document_field_extraction(document_text, fields_to_extract, model_name="gemini-pro"): # gemini-pro for structured extraction
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel(model_name)

    prompt = f"Extract the following fields from the document text as a JSON object: {', '.join(fields_to_extract)}. Document text: {document_text}"

    response = model.generate_content(prompt)
    
    extracted_data = {}
    if response.candidates and hasattr(response.candidates[0], 'content') and response.candidates[0].content.parts:
        # Attempt to parse the response as JSON. The model is prompted to return JSON.
        try:
            import json
            extracted_data = json.loads(response.candidates[0].content.parts[0].text)
        except json.JSONDecodeError:
            extracted_data = {"raw_response": response.candidates[0].content.parts[0].text, "error": "Could not parse model output as JSON"}

    return {"extracted_fields": extracted_data}
