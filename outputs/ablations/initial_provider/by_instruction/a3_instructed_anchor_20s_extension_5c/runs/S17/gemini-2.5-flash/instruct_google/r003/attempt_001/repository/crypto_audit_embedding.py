from google.cloud import aiplatform
from security_client import SecurityClientConfig

def embed_audit_note(project_id: str, location: str, text: str) -> list[float]:
    """Embeds a crypto audit note for semantic search using Google Cloud Vertex AI Embeddings.

    Args:
        project_id: Your Google Cloud project ID.
        location: The GCP region where your Vertex AI endpoint is located (e.g., "us-central1").
        text: The audit note text to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    aiplatform.init(project=project_id, location=location)

    # Using the TextEmbeddingModel to get embeddings.
    # The model name might vary, 'textembedding-gecko@001' is a common one.
    # Ensure this model is available in your specified location.
    try:
        model = aiplatform.language_models.TextEmbeddingModel.from_pretrained("textembedding-gecko@003")
    except Exception as e:
        # Fallback to a different version or raise an informative error
        print(f"Warning: Could not load textembedding-gecko@003, trying textembedding-gecko@001. Error: {e}")
        model = aiplatform.language_models.TextEmbeddingModel.from_pretrained("textembedding-gecko@001")

    embeddings = model.get_embeddings([text])
    # The get_embeddings method returns a list of Embedding objects.
    # We are interested in the values of the first (and only) embedding.
    return embeddings[0].values
