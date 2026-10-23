from typing import List
from google.cloud import aiplatform

def embed_batch(texts: List[str], project_id: str, location: str) -> List[List[float]]:
    """
    Generates embeddings for a batch of texts using Google Cloud Vertex AI.

    Args:
        texts: A list of text strings to embed.
        project_id: Your Google Cloud project ID.
        location: The Google Cloud region (e.g., "us-central1").

    Returns:
        A list of embedding vectors, where each vector is a list of floats.
    """
    aiplatform.init(project=project_id, location=location)
    model = aiplatform.gapic.PredictionServiceClient()
    endpoint = f"projects/{project_id}/locations/{location}/publishers/google/models/text-embedding-004" # Using text-embedding-004 model

    instances = [{"content": text} for text in texts]
    parameters = {"auto_truncate": True} # Example parameter

    response = model.predict(endpoint=endpoint, instances=instances, parameters=parameters)

    embeddings = []
    for prediction in response.predictions:
        embeddings.append(list(prediction["embeddings"]))
    return embeddings
