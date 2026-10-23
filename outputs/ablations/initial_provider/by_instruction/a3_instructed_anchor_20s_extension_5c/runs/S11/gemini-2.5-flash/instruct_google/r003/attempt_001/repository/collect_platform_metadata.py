from google.cloud import aiplatform

def collect_google_metadata(project_id: str, location: str, model_id: str, prompt: str):
    """Invokes a Google Cloud Vertex AI model and collects platform metadata."""
    aiplatform.init(project=project_id, location=location)
    
    # The concrete provider (Google Cloud Vertex AI) is identified by the import and the specific model_id.
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
        endpoint="publishers/google/models/text-bison"
    )
    
    response = aiplatform.gapic.PredictionServiceClient(
        client_options={"api_endpoint": f"{location}-aiplatform.googleapis.com"}
    ).predict(
        endpoint=endpoint,
        instances=[instances],
        parameters=parameters
    )
    
    # Extract relevant metadata. The exact structure of metadata can vary.
    metadata = {
        "model_id": model_id,
        "project_id": project_id,
        "location": location,
        # In Vertex AI, usage metadata is often within the prediction response.
        # This is an example, actual fields might differ.
        "usage_metadata": getattr(response, "metadata", {})
    }
    
    return response.predictions[0], metadata
