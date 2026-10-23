EMBEDDING_MODEL_NAME = "models/embedding-001"


def normalize_embedding_values(embedding_object) -> list[float]:
    """Extracts and normalizes the embedding values from an embedding object."""
    if embedding_object and hasattr(embedding_object, "values"):
        return embedding_object.values
    return []
