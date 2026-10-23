from embeddings_client import (
    get_openai_client,
    DEFAULT_EMBEDDING_MODEL,
    create_batch_embedding_request,
    parse_embedding_response,
)
from embeddings_models import (
    BatchEmbeddingRequest,
    BatchEmbeddingResult,
    parse_openai_response_to_results,
)


def embed_batch(
    texts: list[str],
    model: str = DEFAULT_EMBEDDING_MODEL,
    dimensions: int = None,
    normalize: bool = False,
) -> BatchEmbeddingResult:
    client = get_openai_client()
    request = BatchEmbeddingRequest(texts=texts, model=model, dimensions=dimensions)
    response = client.embeddings.create(**request.to_payload())
    results = parse_openai_response_to_results(response, model=model)
    if normalize:
        from embeddings_models import normalize_vector

        for r in results.results:
            r.vector = normalize_vector(r.vector)
    return results
