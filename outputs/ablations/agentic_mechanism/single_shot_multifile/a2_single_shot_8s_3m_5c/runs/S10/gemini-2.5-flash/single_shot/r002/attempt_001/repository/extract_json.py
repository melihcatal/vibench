import os
import vertexai
from vertexai.generative_models import GenerativeModel, Part, ResponseSchema, StructuralType
from model_client import get_gemini_model
import json

def extract_json(text: str, json_schema: dict) -> dict:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    
    model = get_gemini_model(project_id, location, "gemini-pro")
    
    prompt = f"Extract information from the following text into a JSON object conforming to the provided JSON schema. Only return the JSON object.

Text: {text}

Schema: {json.dumps(json_schema)}"
    
    response_schema_obj = ResponseSchema.from_dict(json_schema)

    response = model.generate_content(
        contents=prompt,
        generation_config={
            "temperature": 0.0,
            "response_mime_type": "application/json"
        }
    )
    
    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        return {}
