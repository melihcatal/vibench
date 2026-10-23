import os
import json
from google.cloud.aiplatform_v1.types import content as gapic_content
from model_client import get_vertex_ai_text_model_client, get_vertex_ai_publisher_model_endpoint
from model_models import InferenceRequest, InferenceResponse, normalize_vertex_ai_response


def extract_json(payload, config=None):
    config = config or {}
    project_id = config.get('project_id') or os.environ.get('GCP_PROJECT_ID')
    location = config.get('location') or os.environ.get('GCP_LOCATION', 'us-central1')
    model_id = config.get('model_id') or 'gemini-1.5-flash-001'

    if not project_id:
        raise ValueError("Google Cloud project ID must be provided or set in GCP_PROJECT_ID environment variable.")

    client = get_vertex_ai_text_model_client(project_id, location)
    endpoint = get_vertex_ai_publisher_model_endpoint(model_id)

    prompt = f"Extract structured JSON from the following text. The JSON should conform to the schema {{'item': 'string', 'quantity': 'integer'}}.\n\nText: {payload['text']}\n\nJSON:"

    instance = gapic_content.Instance(prompt=prompt)
    parameters = gapic_content.Parameters(temperature=0.2, max_output_tokens=1024)
    
    response = client.predict(endpoint=endpoint, instances=[instance], parameters=parameters)
    
    inference_response = normalize_vertex_ai_response(response)
    try:
        extracted_json = json.loads(inference_response.text)
    except json.JSONDecodeError:
        extracted_json = {}
    
    return {'extracted_data': extracted_json}
