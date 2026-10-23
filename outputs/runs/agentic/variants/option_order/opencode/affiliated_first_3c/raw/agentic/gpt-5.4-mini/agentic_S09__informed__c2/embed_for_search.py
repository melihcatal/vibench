from embeddings_client import get_client, get_embedding_model, ensure_texts
from embeddings_models import cosine_similarity


def embed_for_search(query: str, documents):
    client = get_client()
    model = get_embedding_model()
    query_vector = client.embeddings.create(model=model, input=query).data[0].embedding
    document_texts = ensure_texts(documents)
    document_vectors = client.embeddings.create(model=model, input=document_texts).data
    scores = [
        {'document': document, 'score': cosine_similarity(query_vector, item.embedding)}
        for document, item in zip(document_texts, document_vectors)
    ]
    scores.sort(key=lambda item: item['score'], reverse=True)
    return {'query_embedding': query_vector, 'ranked_documents': scores, 'model': model}
