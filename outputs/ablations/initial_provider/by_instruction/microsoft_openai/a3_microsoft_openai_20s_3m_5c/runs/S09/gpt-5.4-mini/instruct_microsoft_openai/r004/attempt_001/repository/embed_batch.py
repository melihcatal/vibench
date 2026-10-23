from embeddings_client import embed_inputs, normalize_text
from embeddings_models import EmbeddingVector, vector_from_response_item


def embed_batch(texts):
    normalized = [normalize_text(text) for text in texts]
    response = embed_inputs(normalized)
    return [EmbeddingVector(text=text, vector=vector_from_response_item(item)) for text, item in zip(normalized, response.data)]
