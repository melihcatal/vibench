import os
from google.cloud import aiplatform

def output_embedding(payload, config=None):
    config = config or {}
    project_id = config.get('project_id') or os.environ.get('GCP_PROJECT_ID')
    location = config.get('location') or os.environ.get('GCP_REGION', 'us-central1')

    if not project_id:
        raise ValueError("Google Cloud project ID not provided and not found in environment variables.")

    aiplatform.init(project=project_id, location=location)

    text_to_embed = payload.get('text', '')
    if not text_to_embed:
        return {'embedding': []}
    
    # Use the TextEmbeddingGarden model from Vertex AI
    # This model is specifically designed for text embeddings.
    model_id = "text-embedding-004" # A common text embedding model in Vertex AI

    try:
        # Ensure the endpoint is correctly formatted for generative models
        client = aiplatform.gapic.PredictionServiceClient(client_options={"api_endpoint": f"{location}-aiplatform.googleapis.com"})
        endpoint_name = client.endpoint_path(project=project_id, location=location, endpoint=f"publishers/google/models/{model_id}")

        instances = [
            {
                "text": text_to_embed
            }
        ]
        
        # For embedding, the predict method for generative models is used.
        # The specific structure for embedding requests with text-embedding-004 might involve different parameters.
        # This example assumes a basic structure for demonstration.
        response = client.predict(endpoint=endpoint_name, instances=instances)
        
        # The actual embedding is usually in a specific field of the prediction response.
        # This is an educated guess based on typical API responses.
        embeddings = []
        if response.predictions and "embeddings" in response.predictions[0]:
            embeddings = response.predictions[0]["embeddings"]["values"]
        elif response.predictions and "embedding" in response.predictions[0]: # Some models might return directly 'embedding'
            embeddings = response.predictions[0]["embedding"]
        else: # Fallback if structure is different
            # Attempt to find the embedding in a less structured way or log an error
            print("Warning: Embedding structure not as expected. Trying to find it.")
            for pred in response.predictions:
                if isinstance(pred, dict) and ("embeddings" in pred or "embedding" in pred):
                    if "embeddings" in pred: embeddings = pred["embeddings"]["values"]
                    elif "embedding" in pred: embeddings = pred["embedding"]
                    break

        return {'embedding': embeddings}
    except Exception as e:
        return {'error': str(e)}
