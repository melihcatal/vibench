from google.cloud import aiplatform

def embed_google_output(project_id: str, location: str, text: str):
    """Embeds platform outputs using Google Cloud Vertex AI embedding models."""
    aiplatform.init(project=project_id, location=location)

    # The concrete provider (Google Cloud Vertex AI) is identified by the import
    # and the specific model ID for embedding.
    model = aiplatform.gapic.PredictionServiceClient(
        client_options={"api_endpoint": f"{location}-aiplatform.googleapis.com"}
    ).endpoint_path(
        project=project_id,
        location=location,
        endpoint="publishers/google/models/text-embedding-004" # Specific embedding model ID
    )

    instances = [{'content': text}]

    response = aiplatform.gapic.PredictionServiceClient(
        client_options={"api_endpoint": f"{location}-aiplatform.googleapis.com"}
    ).predict(
        endpoint=model,
        instances=instances,
        parameters={}
    )

    # Assuming the embedding is in the first prediction's embedding attribute
    if response.predictions and 'embeddings' in response.predictions[0]:
        return response.predictions[0]['embeddings']
    return []
