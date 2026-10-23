
from typing import List

import vertexai
from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel


def embed_translated_segments(
    project_id: str,
    location: str,
    segments: List[str],
) -> List[List[float]]:
    """Embeds a list of translated text segments using Google's Vertex AI.

    Args:
        project_id: Your Google Cloud project ID.
        location: The Google Cloud region (e.g., "us-central1").
        segments: A list of translated text strings to embed.

    Returns:
        A list of embeddings, where each embedding is a list of floats.
    """
    vertexai.init(project=project_id, location=location)
    model = TextEmbeddingModel.from_pretrained("text-embedding-004")
    inputs = [TextEmbeddingInput(text, task_type="SEMANTIC_SIMILARITY") for text in segments]
    embeddings = model.get_embeddings(inputs)
    return [embedding.values for embedding in embeddings]

