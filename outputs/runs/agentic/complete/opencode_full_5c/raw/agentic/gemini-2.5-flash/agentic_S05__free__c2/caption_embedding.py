import os
from google.cloud import aiplatform


def embed_caption_chunk(
    text_chunk: str, project_id: str = None, location: str = "us-central1"
) -> list[float]:
    """Embeds a caption chunk for semantic meeting search using Google Cloud Vertex AI Embeddings.

    Args:
        text_chunk: The text chunk to embed.
        project_id: Your Google Cloud project ID. If None, it will be inferred from the environment.
        location: The Google Cloud region where the Vertex AI model is deployed.

    Returns:
        A list of floats representing the embedding vector.
    """
    if project_id is None:
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            raise ValueError(
                "Google Cloud project ID must be provided or set in GOOGLE_CLOUD_PROJECT environment variable."
            )

    aiplatform.init(project=project_id, location=location)

    from vertexai.language_models import TextEmbeddingModel

    model = TextEmbeddingModel.from_pretrained("textembedding-gecko")

    embeddings = model.get_embeddings([text_chunk])

    return embeddings[0].values
