import os
from typing import List

from google.cloud import aiplatform

def embed_crypto_audit_notes(audit_notes: List[str]) -> List[List[float]]:
    """
    Embeds crypto audit notes using Google Cloud Vertex AI Embeddings API for semantic search.

    Args:
        audit_notes: A list of strings, where each string is a crypto audit note.

    Returns:
        A list of lists of floats, where each inner list is the embedding for a corresponding audit note.
    """
    project_id = os.environ.get("GCP_PROJECT_ID")
    if not project_id:
        raise ValueError("GCP_PROJECT_ID environment variable not set.")

    location = os.environ.get("GCP_REGION", "us-central1") # Default to us-central1

    aiplatform.init(project=project_id, location=location)

    # Use the TextEmbeddingModel for text embeddings.
    # The model identifier makes the provider concrete and identifiable.
    model = aiplatform.gapic.PredictionServiceClient(client_options={"api_endpoint": f"{location}-aiplatform.googleapis.com"})
    endpoint = f"projects/{project_id}/locations/{location}/publishers/google/models/multimodalembedding@001"

    instances = [{"text_content": note} for note in audit_notes]
    
    response = model.predict(endpoint=endpoint, instances=instances)
    
    embeddings = []
    for prediction in response.predictions:
        embeddings.append(list(prediction["textEmbedding"]))
        
    return embeddings

