import math
import os
import cohere

from embeddings_client import get_embedding_client, DEFAULT_MODEL
from embeddings_models import normalize_embedding_result


def _cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return 0.0 if na == 0.0 or nb == 0.0 else dot / (na * nb)


def similarity_score(text_a: str, text_b: str):
    client = get_embedding_client()
    model = os.getenv("COHERE_EMBED_MODEL", DEFAULT_MODEL)
    response = client.embed(texts=[text_a, text_b], model=model, input_type="search_document")
    vectors = normalize_embedding_result(response)
    return _cosine_similarity(vectors[0], vectors[1])

