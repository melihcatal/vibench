from typing import List, Tuple
from embeddings_client import get_embeddings_client

EMBEDDING_MODEL = "text-embedding-3-small"

def embed_for_search(query: str, documents: List[str]) -> Tuple[List[float], List[List[float]]]:
    client = get_embeddings_client()
    query_response = client.embeddings.create(model=EMBEDDING_MODEL, input=query)
    query_emb = query_response.data[0].embedding
    docs_response = client.embeddings.create(model=EMBEDDING_MODEL, input=documents)
    docs_embs = [data.embedding for data in docs_response.data]
    return query_emb, docs_embs