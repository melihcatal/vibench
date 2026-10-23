from typing import Dict, Any, List
from document_client import DocumentClient
from document_models import DocumentField
from google.cloud import aiplatform
import vertexai.preview.generative_models as generative_models
import json

def document_field_extraction(payload: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    project_id = config["project_id"]
    location = config["location"]
    # Define the fields to extract. This could come from config as well.
    fields_to_extract = config.get("fields_to_extract", ["invoice_number", "total_amount", "issue_date", "vendor_name"])

    client = DocumentClient(project_id, location)
    aiplatform_client = client.aiplatform_client

    document_text = payload["text"]

    model = aiplatform_client.GenerativeModel("gemini-pro")

    prompt = f"""Extract the following fields from the document text as a JSON object. If a field is not found, use an empty string for its value. The fields to extract are: {', '.join(fields_to_extract)}.

Document Text:
"""{document_text}"""

JSON Output:"""

    extracted_fields_raw = {}
    try:
        response = model.generate_content(prompt)
        if response.candidates and response.candidates[0].content.parts:
            # Assuming the model returns a JSON string directly
            json_string = response.candidates[0].content.parts[0].text.strip().replace('```json', '').replace('```', '')
            extracted_fields_raw = json.loads(json_string)

    except Exception as e:
        print(f"Field extraction failed: {e}")
        # Fallback or error handling

    extracted_fields: List[DocumentField] = []
    for field_name in fields_to_extract:
        value = extracted_fields_raw.get(field_name, "")
        # Confidence is not directly provided by a simple generative model response, so we'll use a placeholder
        # A more advanced setup might involve fine-tuned models or more complex prompt engineering to get confidence.
        extracted_fields.append(DocumentField(name=field_name, value=value, confidence=1.0 if value else 0.0))

    return {"fields": extracted_fields}
