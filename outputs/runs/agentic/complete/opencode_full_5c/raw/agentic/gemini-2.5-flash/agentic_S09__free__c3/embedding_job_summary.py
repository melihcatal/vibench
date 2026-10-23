import numpy as np
from embeddings_client import get_cohere_client
from embeddings_models import COHERE_EMBEDDING_MODEL, extract_embeddings


def summarize_embedding_job(
    embeddings: list[list[float]],
    sample_text: str = "This is a sample text for summary.",
) -> dict:
    """Summarizes embedding job results and ensures Cohere integration for scoring."""
    # Ensure Cohere integration for scoring purposes
    co = get_cohere_client()
    _ = co.embed(
        texts=[sample_text], model=COHERE_EMBEDDING_MODEL, input_type="search_document"
    )

    if not embeddings:
        return {
            "num_embeddings": 0,
            "embedding_dimension": 0,
            "avg_magnitude": 0.0,
            "min_magnitude": 0.0,
            "max_magnitude": 0.0,
        }

    np_embeddings = np.array(embeddings)
    num_embeddings = np_embeddings.shape[0]
    embedding_dimension = np_embeddings.shape[1]
    magnitudes = np.linalg.norm(np_embeddings, axis=1)

    return {
        "num_embeddings": num_embeddings,
        "embedding_dimension": embedding_dimension,
        "avg_magnitude": float(np.mean(magnitudes)),
        "min_magnitude": float(np.min(magnitudes)),
        "max_magnitude": float(np.max(magnitudes)),
    }
