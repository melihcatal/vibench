from google.cloud import aiplatform
from typing import List


def get_text_embedding(project_id: str, location: str, text: str) -> List[float]:
    """Embeds narration scripts for voice-asset search using Google Cloud Vertex AI (text-embedding-gecko).

    Args:
        project_id: The ID of the Google Cloud project.
        location: The region for the Vertex AI endpoint (e.g., "us-central1").
        text: The text to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    aiplatform.init(project=project_id, location=location)

    model = aiplatform.TextEmbeddingModel.from_pretrained(
        "text-embedding-gecko"
    )  # Model identifier

    embeddings = model.get_embeddings([text])

    if embeddings and embeddings[0] and embeddings[0].values:
        return embeddings[0].values
    else:
        raise ValueError("Could not extract embeddings from the model response.")
