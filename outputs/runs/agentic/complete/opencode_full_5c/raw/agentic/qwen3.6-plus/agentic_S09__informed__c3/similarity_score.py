from embeddings_client import get_openai_client, DEFAULT_EMBEDDING_MODEL
from embeddings_models import (
    EmbeddingRequest,
    parse_openai_response_to_results,
    cosine_similarity,
)


def similarity_score(
    text_a: str,
    text_b: str,
    model: str = DEFAULT_EMBEDDING_MODEL,
    dimensions: int = None,
) -> float:
    client = get_openai_client()
    response = client.embeddings.create(
        input=[text_a, text_b],
        model=model,
        dimensions=dimensions,
    )
    batch_result = parse_openai_response_to_results(response, model=model)
    vec_a = batch_result.get_vector(0)
    vec_b = batch_result.get_vector(1)
    return cosine_similarity(vec_a, vec_b)
