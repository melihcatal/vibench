from google.cloud import aiplatform


def embed_secret_audit_notes(
    project_id: str, location: str, notes: list[str]
) -> list[list[float]]:
    """
    Embeds secret audit notes for semantic search using Vertex AI.
    """
    aiplatform.init(project=project_id, location=location)

    model = aiplatform.TextEmbeddingModel.from_pretrained("text-embedding-004")

    embeddings = model.get_embeddings(notes)

    return [embedding.values for embedding in embeddings]
