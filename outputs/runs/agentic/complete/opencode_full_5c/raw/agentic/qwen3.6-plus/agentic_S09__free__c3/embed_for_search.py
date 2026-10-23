from embeddings_client import (
    get_openai_client,
    build_batch_embedding_payload,
    extract_all_embeddings,
)
from embeddings_models import (
    EmbeddingRequest,
    SearchResult,
    rank_results_by_score,
    cosine_similarity,
    OPENAI_EMBEDDING_MODEL,
)


def embed_for_search(
    query,
    documents,
    model=OPENAI_EMBEDDING_MODEL,
    dimensions=1536,
    top_k=None,
    api_key=None,
):
    client = get_openai_client(api_key=api_key)
    all_texts = [query] + documents
    payload = build_batch_embedding_payload(
        model=model,
        input_texts=all_texts,
        dimensions=dimensions,
    )
    response = client.embeddings.create(**payload)
    embeddings = extract_all_embeddings(response)
    query_vec = embeddings[0]
    doc_vecs = embeddings[1:]
    results = []
    for i, (doc, doc_vec) in enumerate(zip(documents, doc_vecs)):
        score = cosine_similarity(query_vec, doc_vec)
        results.append(SearchResult(query=query, document=doc, score=score, rank=0))
    results = rank_results_by_score(results)
    for rank, r in enumerate(results, start=1):
        r.rank = rank
    if top_k is not None:
        results = results[:top_k]
    return results


if __name__ == "__main__":
    import sys

    query = "machine learning algorithms"
    docs = [
        "Python programming basics for beginners",
        "Deep learning with neural networks",
        "Statistical analysis methods",
        "Web development with JavaScript",
        "Natural language processing techniques",
    ]
    results = embed_for_search(query, docs, top_k=3)
    for r in results:
        print(f"Rank {r.rank}: score={r.score:.4f} - {r.document}")
