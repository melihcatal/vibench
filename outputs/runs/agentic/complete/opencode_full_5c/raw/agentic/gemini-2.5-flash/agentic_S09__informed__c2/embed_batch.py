from typing import List
from embeddings_client import get_gemini_embeddings_client
from embeddings_models import normalize_embedding_response


def embed_batch(texts: List[str]) -> List[List[float]]:
    """Generates embedding vectors for a batch of text strings using Google Gemini Embeddings."""
    model = get_gemini_embeddings_client()
    response = model.embed_content(content=texts, task_type="SEMANTIC_SIMILARITY")
    embedding_response = normalize_embedding_response(response)
    return embedding_response.embeddings
