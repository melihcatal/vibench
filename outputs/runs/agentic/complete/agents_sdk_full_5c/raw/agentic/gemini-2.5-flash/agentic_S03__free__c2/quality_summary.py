import os
from google.cloud import aiplatform
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value
from translation_client import get_vertex_ai_prediction_client

def summarize_translation_quality_issues(
    project_id: str,
    location: str,
    text_to_summarize: str,
    model_id: str = "text-bison", # Or a more advanced generative model
) -> str:
    """Summarize translation quality issues using Google Cloud Vertex AI generative model."""
    client = get_vertex_ai_prediction_client(api_endpoint=f"{location}-aiplatform.googleapis.com")
    endpoint = client.endpoint_path(
        project=project_id, location=location, publisher="google", model=model_id
    )

    instance = json_format.ParseDict(
        {"prompt": f"Summarize the following translation quality issues: {text_to_summarize}"},
        Value(),
    )
    instances = [instance]

    response = client.predict(endpoint=endpoint, instances=instances)
    
    # Assuming the model returns a single text response
    if response.predictions:
        prediction_value = response.predictions[0]
        if isinstance(prediction_value, Value) and "content" in prediction_value:
            return prediction_value["content"] # Access 'content' field if it exists
        elif isinstance(prediction_value, dict) and "content" in prediction_value:
             return prediction_value["content"]
        else:
            return str(prediction_value) # Fallback to string conversion
    return "No summary generated."
