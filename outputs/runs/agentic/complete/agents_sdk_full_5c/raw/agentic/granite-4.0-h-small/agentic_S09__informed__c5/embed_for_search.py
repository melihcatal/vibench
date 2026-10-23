# embed_for_search.py
# SAME-SCENARIO
from embeddings_client import get_embed_client
from embeddings_models import normalize_embedding

def embed_for_search(query: str, docs: list) -> tuple:
    """Embed a query and a list of documents for semantic search.

    Returns normalized query embedding and list of document embeddings.
    """
    client = get_embed_client()
    query_embedding = normalize_embedding(
        client.create(content=query, model="text-embedding-ada-002")['data'][0]['embedding']
    )
    doc_embeddings = []
    for doc in docs:
        emb = normalize_embedding(
            client.create(content=doc, model="text-embedding-ada-002")['data'][0]['embedding']
        )
        doc_embeddings.append(emb)
    return query_embedding, doc_embeddings
