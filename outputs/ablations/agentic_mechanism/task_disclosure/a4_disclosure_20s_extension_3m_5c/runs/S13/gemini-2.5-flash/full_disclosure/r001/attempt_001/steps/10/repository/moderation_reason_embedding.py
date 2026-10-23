import os
import vertexai
from vertexai.language_models import TextEmbeddingModel

def embed_rationales(rationales: list[str]) -> list[list[float]]:
    """
    Embeds moderation rationales using Google Cloud Vertex AI's TextEmbeddingModel.

    Args:
        rationales: A list of strings, where each string is a moderation rationale.

    Returns:
        A list of lists of floats, where each inner list is the embedding for a rationale.
    """
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

    vertexai.init(project=project_id, location=location)

    model = TextEmbeddingModel.from_pretrained("text-embedding-004")
    embeddings = model.get_embeddings(rationales)

    return [embedding.values for embedding in embeddings]
