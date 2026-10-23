from embeddings_client import create_embeddings_client, handle_embedding_error
from embeddings_models import (
    EmbeddingRequest,
    EmbeddingResponse,
    batch_cosine_similarities,
)


def embed_for_search(
    query, documents, model=None, client=None, api_key=None, top_k=None
):
    if not query or not query.strip():
        raise ValueError("query must be a non-empty string")
    if not documents:
        raise ValueError("documents list must not be empty")

    if client is None:
        client, model = create_embeddings_client(model=model, api_key=api_key)

    if model is None:
        model = "text-embedding-3-small"

    all_texts = [query] + list(documents)

    request = EmbeddingRequest(
        texts=all_texts,
        model=model,
    )

    try:
        response = client.embeddings.create(**request.to_payload())
        result = EmbeddingResponse.from_openai_response(response)
    except Exception as exc:
        handle_embedding_error(exc)

    query_vec = result.get_embedding(0)
    doc_vecs = [result.get_embedding(i + 1) for i in range(len(documents))]

    similarities = batch_cosine_similarities(query_vec, doc_vecs)

    scored_docs = []
    for idx, (doc, score) in enumerate(zip(documents, similarities)):
        scored_docs.append(
            {
                "document": doc,
                "similarity_score": score,
                "index": idx,
                "embedding": doc_vecs[idx],
            }
        )

    scored_docs.sort(key=lambda x: x["similarity_score"], reverse=True)

    if top_k is not None:
        scored_docs = scored_docs[:top_k]

    return {
        "query": query,
        "query_embedding": query_vec,
        "results": scored_docs,
        "model": model,
        "total_documents": len(documents),
        "usage": result.usage,
    }
