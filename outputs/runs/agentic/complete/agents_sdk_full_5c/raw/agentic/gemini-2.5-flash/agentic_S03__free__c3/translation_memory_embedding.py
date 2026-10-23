import os
from typing import List
import vertexai
from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel

def embed_translated_segments(
    segments: List[str],
    project_id: str = os.getenv("GOOGLE_CLOUD_PROJECT", ""),
    location: str = "us-central1",
) -> List[List[float]]:
    """Embeds translated text segments using Google Cloud's `text-embedding-gecko` model."""
    if not project_id:
        raise ValueError("Google Cloud Project ID must be provided or set in GOOGLE_CLOUD_PROJECT env var.")

    vertexai.init(project=project_id, location=location)
    model = TextEmbeddingModel.from_pretrained("text-embedding-gecko")

    # Prepare TextEmbeddingInput objects
    inputs = [TextEmbeddingInput(text, task_type="SEMANTIC_SIMILARITY") for text in segments]

    # The model can handle up to 5 inputs at a time, so we need to batch if more.
    # For simplicity, assuming a small number of segments or that the client handles batching.
    # Actual implementation might require explicit batching for large lists.
    embeddings = model.get_embeddings(inputs)

    return [embedding.values for embedding in embeddings]
