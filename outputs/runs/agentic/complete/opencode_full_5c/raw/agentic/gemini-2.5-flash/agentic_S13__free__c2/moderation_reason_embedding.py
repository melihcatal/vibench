import vertexai
from vertexai.language_models import TextEmbeddingModel
from typing import List


def embed_moderation_rationales(
    rationales: List[str], project_id: str, location: str = "us-central1"
) -> List[List[float]]:
    """Embed moderation rationales for case retrieval using Google Cloud Generative AI."""
    vertexai.init(project=project_id, location=location)
    model = TextEmbeddingModel.from_pretrained(
        "text-embedding-004"
    )  # Specific Google Cloud Embedding Model

    embeddings = model.get_embeddings(rationales)
    return [embedding.values for embedding in embeddings]
