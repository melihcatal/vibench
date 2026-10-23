from google.cloud import aiplatform
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class EmbeddingResponse:
    embeddings: List[List[float]]
    model: str
    dimensions: int


def asset_metadata_embedding(
    text: str,
    project_id: str,
    location: str = "us-central1",
    model_id: str = "textembedding-gecko@latest",
) -> EmbeddingResponse:
    """
    Embeds object metadata and extracted text for search using Google Vertex AI.

    Args:
        text: Text to embed.
        project_id: Google Cloud project ID.
        location: Vertex AI location (e.g., "us-central1").
        model_id: Vertex AI embedding model ID (e.g., "textembedding-gecko@latest").

    Returns:
        EmbeddingResponse containing embeddings, model used, and dimensions.
    """
    aiplatform.init(project=project_id, location=location)
    model = aiplatform.TextEmbeddingModel.from_pretrained(model_id)

    embeddings = model.get_embeddings([text])
    embedding = embeddings[0].values

    return EmbeddingResponse(
        embeddings=[embedding], model=model_id, dimensions=len(embedding)
    )
