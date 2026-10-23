from embeddings_client import embed_inputs, normalize_text
from embeddings_models import EmbeddingVector, vector_from_response_item


def embed_text(text: str) -> EmbeddingVector:
    normalized = normalize_text(text)
    response = embed_inputs([normalized])
    return EmbeddingVector(text=normalized, vector=vector_from_response_item(response.data[0]))
