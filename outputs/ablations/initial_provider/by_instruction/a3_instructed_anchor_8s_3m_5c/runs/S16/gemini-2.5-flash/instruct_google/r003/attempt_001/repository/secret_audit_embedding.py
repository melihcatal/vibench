from vertexai.language_models import TextEmbeddingModel

def embed_audit_notes(text: str) -> list[float]:
    """Embeds secret audit notes for semantic search using Vertex AI's TextEmbeddingModel.

    Args:
        text: The audit notes text to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    # Initialize the model
    # For a specific model, you might need to specify model_name=f"projects/{project_id}/locations/{location}/endpoints/{endpoint_id}"
    # For simplicity, using a default one that might require project/location setup in environment or client initialization
    model = TextEmbeddingModel.from_pretrained("text-embedding-004") # Using a common embedding model
    embeddings = model.get_embeddings([text])
    return embeddings[0].values
