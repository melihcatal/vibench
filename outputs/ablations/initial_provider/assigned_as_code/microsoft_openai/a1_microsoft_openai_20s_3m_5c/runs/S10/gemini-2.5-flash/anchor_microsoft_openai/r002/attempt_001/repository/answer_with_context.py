import os
from google.cloud.aiplatform_v1.types import content as gapic_content
from model_client import get_vertex_ai_text_model_client, get_vertex_ai_publisher_model_endpoint
from model_models import InferenceRequest, InferenceResponse, normalize_vertex_ai_response


def answer_with_context(payload, config=None):
    config = config or {}
    project_id = config.get('project_id') or os.environ.get('GCP_PROJECT_ID')
    location = config.get('location') or os.environ.get('GCP_LOCATION', 'us-central1')
    model_id = config.get('model_id') or 'gemini-1.5-flash-001'

    if not project_id:
        raise ValueError("Google Cloud project ID must be provided or set in GCP_PROJECT_ID environment variable.")

    client = get_vertex_ai_text_model_client(project_id, location)
    endpoint = get_vertex_ai_publisher_model_endpoint(model_id)

    context = payload.get('context', '')
    question = payload.get('question', '')

    prompt = f"Given the following context, answer the question. If the answer is not in the context, state that you don't know.\n\nContext: {context}\n\nQuestion: {question}\n\nAnswer:"

    instance = gapic_content.Instance(prompt=prompt)
    parameters = gapic_content.Parameters(temperature=0.2, max_output_tokens=512)
    
    response = client.predict(endpoint=endpoint, instances=[instance], parameters=parameters)
    
    inference_response = normalize_vertex_ai_response(response)
    
    return {'answer': inference_response.text}
