from typing import List, Dict
from embeddings_client import EmbeddingsClient

def embed_for_search(query: str, documents: List[str]) -> Dict[str, List]:
    client = EmbeddingsClient()
    query_emb = client.embed_texts([query])[0]
    doc_embs = client.embed_texts(documents)
    return {"query_embedding": query_emb, "document_embeddings": doc_embs}
