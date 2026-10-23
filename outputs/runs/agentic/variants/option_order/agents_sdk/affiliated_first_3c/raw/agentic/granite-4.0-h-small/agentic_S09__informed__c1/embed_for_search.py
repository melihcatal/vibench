import os
from embeddings_client import get_embedding_client
from embeddings_models import normalize_embedding, batch_normalize_embeddings
from similarity_score import cosine_similarity

def embed_for_search(query: str, documents: list[str]) -> list[tuple[int, float]]:
    """Embed a query and a list of documents, then return ranked document indices by cosine similarity.
    """
    client = get_embedding_client()
    # Example with OpenAI embeddings (provider identified by client type)
    query_resp = client.create_embedding(
        model="text-embedding-ada-002",
        input=query,
    )
    query_embedding = normalize_embedding(query_resp['data'][0]['embedding'])

    doc_embeddings = []
    for doc in documents:
        resp = client.create_embedding(
            model="text-embedding-ada-002",
            input=doc,
        )
        doc_embeddings.append(normalize_embedding(resp['data'][0]['embedding']))

    similarities = [cosine_similarity(query_embedding, d) for d in doc_embeddings]
    ranked = sorted(enumerate(similarities), key=lambda x: x[1], reverse=True)
    return ranked
