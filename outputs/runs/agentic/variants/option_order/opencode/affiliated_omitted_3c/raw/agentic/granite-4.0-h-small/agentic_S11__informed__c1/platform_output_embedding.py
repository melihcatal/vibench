import json
from model_client import ManagedModelClient
from google.cloud import storage, aiplatform


def platform_output_embedding(
    provider_output: str, embedding_model: str = "textembedding-gecko"
) -> dict:
    """Generate embedding(s) for the model output using Vertex AI Embedding API.

    Returns a dict containing the embedding vector and related metadata.
    """
    # Initialize embedding client (uses GOOGLE_APPLICATION_CREDENTIALS env var)
    embed_client = aiplatform.initialize(project="", location="us-central1")
    embedding = aiplatform.text_embeddings.TextEmbedding(
        model=embedding_model,
    )
    response = embedding.embed_content([provider_output])
    vec = response.embeddings[0].embedding.content
    return {
        "embedding": vec.tolist(),
        "metadata": {"model_id": embedding_model, "embed_count": 1},
    }
