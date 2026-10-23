import math
import os
from embeddings_client import get_embeddings_client
from embeddings_models import normalize_embedding_response, EmbeddingRequest

MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def cosine_similarity(vec_a, vec_b):
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))
    return dot / (norm_a * norm_b) if norm_a and norm_b else 0.0


def similarity_score(text_a: str, text_b: str):
    client = get_embeddings_client()
    req = EmbeddingRequest(input=[text_a, text_b], model=MODEL)
    response = client.embeddings.create(model=req.model, input=req.input)
    normalized = normalize_embedding_response(response)
    return cosine_similarity(normalized[0], normalized[1])
