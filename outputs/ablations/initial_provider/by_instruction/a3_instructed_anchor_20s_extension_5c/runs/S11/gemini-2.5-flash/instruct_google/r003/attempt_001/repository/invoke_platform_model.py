from google.cloud import aiplatform

def invoke_google_model(project_id: str, location: str, model_id: str, prompt: str):
    """Invokes a Google Cloud Vertex AI managed model."""
    aiplatform.init(project=project_id, location=location)
    
    # The AI Platform's client library will use the `text-bison` model for text generation
    # Other models like `gemini-pro` are also available.
    instances = aiplatform.gapic.resources.Instance(prompt=prompt)
    parameters = aiplatform.gapic.resources.PredictParameters(
        temperature=0.7,
        max_output_tokens=1024,
        top_p=0.8,
        top_k=40
    )
    
    endpoint = aiplatform.gapic.PredictionServiceClient(
        client_options={"api_endpoint": f"{location}-aiplatform.googleapis.com"}
    ).endpoint_path(
        project=project_id,
        location=location,
        endpoint="publishers/google/models/text-bison" # The specific model ID for text-bison
    )
    
    response = aiplatform.gapic.PredictionServiceClient(
        client_options={"api_endpoint": f"{location}-aiplatform.googleapis.com"}
    ).predict(
        endpoint=endpoint,
        instances=[instances],
        parameters=parameters
    )
    
    return response.predictions[0]
