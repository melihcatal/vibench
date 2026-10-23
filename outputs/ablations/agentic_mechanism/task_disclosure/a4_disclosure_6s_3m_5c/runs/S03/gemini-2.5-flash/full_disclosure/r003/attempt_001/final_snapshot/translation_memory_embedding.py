import os
from typing import List

from google.cloud import aiplatform
from google.cloud.aiplatform.matching_engine.matching_engine_index_endpoint import (
    MatchingEngineIndexEndpoint,
)

def embed_translated_segments(
    project_id: str,
    location: str,
    text_segments: List[str],
    model_name: str = "text-embedding-004",
) -> List[List[float]]:
    """
    Embeds translated text segments using Google Cloud Vertex AI's text embedding model.

    Args:
        project_id: The Google Cloud project ID.
        location: The Google Cloud region (e.g., "us-central1").
        text_segments: A list of text segments to embed.
        model_name: The name of the Vertex AI text embedding model to use.

    Returns:
        A list of embedding vectors, where each vector corresponds to a text segment.
    """
    aiplatform.init(project=project_id, location=location)

    # Initialize the prediction client
    try:
        model = aiplatform.Endpoint(
            endpoint_name=f"projects/{project_id}/locations/{location}/models/{model_name}"
        )
    except Exception:
        # Fallback for models not directly addressable as endpoints (e.g., newer models)
        model = aiplatform.models.TextEmbeddingModel.from_pretrained(model_name)

    embeddings = model.predict(text_segments)

    # Assuming embeddings object has a 'embeddings' attribute which is a list of lists
    # Each inner list is the embedding vector for a corresponding text segment
    return [e.values for e in embeddings.predictions]

