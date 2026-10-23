from embed_batch import embed_batch
from embeddings_models import SearchResult, cosine_similarity


def embed_for_search(
    query, documents, model=None, dimensions=None, api_key=None, top_k=None
):
    all_texts = [query] + documents
    batch_resp = embed_batch(
        all_texts, model=model, dimensions=dimensions, api_key=api_key
    )
    query_embedding = batch_resp.embeddings[0]
    doc_embeddings = batch_resp.embeddings[1:]
    doc_objects = []
    for i, doc_text in enumerate(documents):
        score = cosine_similarity(query_embedding, doc_embeddings[i])
        doc_objects.append({"text": doc_text, "score": score, "index": i})
    doc_objects.sort(key=lambda d: d["score"], reverse=True)
    if top_k is not None:
        doc_objects = doc_objects[:top_k]
    return SearchResult(
        query=query,
        query_embedding=query_embedding,
        documents=doc_objects,
        ranked_results=doc_objects,
    )
