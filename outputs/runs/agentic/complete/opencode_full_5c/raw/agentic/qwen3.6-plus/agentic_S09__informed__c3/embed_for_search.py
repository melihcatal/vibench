from embeddings_client import get_openai_client, DEFAULT_EMBEDDING_MODEL
from embeddings_models import (
    BatchEmbeddingRequest,
    parse_openai_response_to_results,
    cosine_similarity,
)


def embed_for_search(
    query: str,
    documents: list[str],
    model: str = DEFAULT_EMBEDDING_MODEL,
    dimensions: int = None,
) -> dict:
    client = get_openai_client()
    all_texts = [query] + documents
    request = BatchEmbeddingRequest(texts=all_texts, model=model, dimensions=dimensions)
    response = client.embeddings.create(**request.to_payload())
    batch_result = parse_openai_response_to_results(response, model=model)
    query_vector = batch_result.get_vector(0)
    doc_vectors = [batch_result.get_vector(i + 1) for i in range(len(documents))]
    scores = []
    for i, doc_vector in enumerate(doc_vectors):
        score = cosine_similarity(query_vector, doc_vector)
        scores.append({"document": documents[i], "index": i, "similarity": score})
    scores.sort(key=lambda x: x["similarity"], reverse=True)
    return {
        "query": query,
        "model": model,
        "ranked_results": scores,
    }
