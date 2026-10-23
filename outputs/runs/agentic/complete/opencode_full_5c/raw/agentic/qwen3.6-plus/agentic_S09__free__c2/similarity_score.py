from embeddings_client import create_embeddings_client, handle_embedding_error
from embeddings_models import (
    EmbeddingRequest,
    EmbeddingResponse,
    SimilarityResult,
    cosine_similarity,
)


def similarity_score(text_a, text_b, model=None, client=None, api_key=None):
    if not text_a or not text_a.strip():
        raise ValueError("text_a must be a non-empty string")
    if not text_b or not text_b.strip():
        raise ValueError("text_b must be a non-empty string")

    if client is None:
        client, model = create_embeddings_client(model=model, api_key=api_key)

    if model is None:
        model = "text-embedding-3-small"

    request = EmbeddingRequest(
        texts=[text_a, text_b],
        model=model,
    )

    try:
        response = client.embeddings.create(**request.to_payload())
        result = EmbeddingResponse.from_openai_response(response)
        vec_a = result.get_embedding(0)
        vec_b = result.get_embedding(1)
    except Exception as exc:
        handle_embedding_error(exc)

    score = cosine_similarity(vec_a, vec_b)

    norm_a = sum(x * x for x in vec_a) ** 0.5
    norm_b = sum(x * x for x in vec_b) ** 0.5
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))

    return SimilarityResult(
        score=score,
        vector_a_norm=norm_a,
        vector_b_norm=norm_b,
        dot_product=dot_product,
    )
