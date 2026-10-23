import os
from embeddings_client import get_client
from embeddings_models import normalize_embedding

def embed_for_search(query: str, documents: list[str]):
    """Embed a query and a list of document texts for semantic search.

    Returns:
        tuple: (query_embedding, doc_embeddings) where both are normalized.
    """
    client = get_client()
    # Using OpenAI embeddings (identified by SDK import/model name)
    query_response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=query,
    )
    query_vec = normalize_embedding(query_response['data'][0]['embedding'])

    doc_embeddings = []
    for doc in documents:
        resp = client.embeddings.create(
            model="text-embedding-ada-002",
            input=doc,
        )
        vec = normalize_embedding(resp['data'][0]['embedding'])
        doc_embeddings.append(vec)
    return query_vec, doc_embeddings
