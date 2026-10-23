from google.cloud import aiplatform

def embed_batch(texts: list[str], project_id: str, location: str) -> list[list[float]]:
    """Generates embeddings for a batch of text strings using Vertex AI.

    Args:
        texts: A list of text strings to embed.
        project_id: Your Google Cloud project ID.
        location: The Google Cloud region (e.g., "us-central1").

    Returns:
        A list of embedding vectors, where each vector is a list of floats.
    """
    aiplatform.init(project=project_id, location=location)

    # The model ID for text embeddings. You might need to adjust this based on available models.
    # As of the last update, "text-embedding-004" is a common choice.
    model_id = "text-embedding-004" 
    model = aiplatform.get_model_deployment("publishers/google/models/text-embedding-004")

    instances = [{"content": text} for text in texts]
    
    # Use the endpoint directly for batch prediction
    endpoint_name = f"projects/{project_id}/locations/{location}/endpoints/787268802951478272" # Example endpoint, replace if necessary
    
    response = model.predict(instances=instances)
    
    embeddings = []
    for prediction in response.predictions:
        embeddings.append(prediction["embeddings"]["values"])
        
    return embeddings
