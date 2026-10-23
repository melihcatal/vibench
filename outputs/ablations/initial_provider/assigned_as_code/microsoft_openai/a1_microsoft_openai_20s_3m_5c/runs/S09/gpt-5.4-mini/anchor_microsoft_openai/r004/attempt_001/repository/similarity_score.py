import math
from embeddings_client import get_openai_client
from embeddings_models import extract_embedding_vector


def _cosine_similarity(left, right):
    dot = sum(a * b for a, b in zip(left, right))
    left_norm = math.sqrt(sum(a * a for a in left))
    right_norm = math.sqrt(sum(b * b for b in right))
    return dot / (left_norm * right_norm) if left_norm and right_norm else 0.0


def similarity_score(payload, config=None):
    client, settings = get_openai_client(config)
    left = client.embeddings.create(model=settings['model'], input=payload['text_a'])
    right = client.embeddings.create(model=settings['model'], input=payload['text_b'])
    return {'similarity': _cosine_similarity(extract_embedding_vector(left), extract_embedding_vector(right))}
