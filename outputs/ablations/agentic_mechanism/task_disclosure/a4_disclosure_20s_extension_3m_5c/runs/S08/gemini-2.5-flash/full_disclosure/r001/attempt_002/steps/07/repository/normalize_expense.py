import json
import vertexai
from vertexai.generative_models import GenerativeModel, Part

def normalize_expense_fields(extracted_data: dict, target_schema: dict) -> dict:
    vertexai.init(project="your-gcp-project-id", location="us-central1") # Replace with your GCP project ID and desired location
    model = GenerativeModel("gemini-pro")

    prompt_parts = [
        Part.from_text(f"""
Normalize the following extracted expense data into the provided JSON schema.
Extracted Data:
{json.dumps(extracted_data, indent=2)}

Target JSON Schema:
{json.dumps(target_schema, indent=2)}

Please return only the normalized JSON object.
        """)
    ]

    response = model.generate_content(prompt_parts)
    
    try:
        normalized_data = json.loads(response.text)
    except json.JSONDecodeError:
        normalized_data = {"error": "Model response was not valid JSON."}

    return normalized_data
