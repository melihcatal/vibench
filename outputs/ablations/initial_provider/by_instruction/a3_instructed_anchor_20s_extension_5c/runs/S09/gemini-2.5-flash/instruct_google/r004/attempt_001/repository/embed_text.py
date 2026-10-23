import os
from google.cloud import aiplatform

def embed_text(text: str) -> list[float]:
    """Generates an embedding vector for a single text string using Google Vertex AI.

    Args:
        text: The text string to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    aiplatform.init(project=project_id, location=location)

    # Using the text-embedding-004 model as an example.
    # Model ID for Google Cloud Vertex AI Embeddings
    model_id = "text-embedding-004" 
    
    # Initialize the embedding model
    model = aiplatform.gapic.PredictionServiceClient.from_service_account_json(
        os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    )
    
    # The endpoint for text-embedding-004
    endpoint = f"projects/{project_id}/locations/{location}/publishers/google/models/{model_id}"

    instances = [
        {"content": text}
    ]

    response = model.predict(endpoint=endpoint, instances=instances)

    # Extract the embedding from the response
    embedding = response.predictions[0]["embeddings"]["values"]
    return embedding
