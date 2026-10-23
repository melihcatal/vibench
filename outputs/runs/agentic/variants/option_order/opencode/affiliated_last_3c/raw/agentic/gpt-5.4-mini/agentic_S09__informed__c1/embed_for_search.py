from embeddings_client import get_client, get_embedding_model, normalize_texts
from embeddings_models import cosine_similarity


def embed_for_search(query: str, documents):
    client = get_client()
    payload = normalize_texts([query] + list(documents))
    response = client.embeddings.create(model=get_embedding_model(), input=payload)
    query_vector = response.data[0].embedding
    doc_vectors = [item.embedding for item in response.data[1:]]
    ranked = sorted(
        zip(documents, doc_vectors),
        key=lambda item: cosine_similarity(query_vector, item[1]),
        reverse=True,
    )
    return {"query_embedding": query_vector, "ranked_documents": ranked}
