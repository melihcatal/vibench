from embeddings_client import create_client, embedding_request_kwargs
from embeddings_models import cosine_similarity, normalize_vector


def similarity_score(text_a: str, text_b: str) -> float:
    client = create_client()
    response = client.embeddings.create(
        input=[text_a, text_b], **embedding_request_kwargs()
    )
    left = normalize_vector(response.data[0].embedding)
    right = normalize_vector(response.data[1].embedding)
    return cosine_similarity(left, right)
