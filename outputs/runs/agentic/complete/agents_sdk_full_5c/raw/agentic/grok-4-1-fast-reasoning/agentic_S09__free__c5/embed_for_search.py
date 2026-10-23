from typing import List, Dict
from embeddings_client import client
from embeddings_models import MODEL_ID, normalize_embedding

def embed_for_search(query: str, documents: List[str]) -> Dict:
    query_resp = client.embeddings.create(model=MODEL_ID, input=query)
    query_emb = normalize_embedding(query_resp.data[0].embedding)
    
    if documents:
        doc_resp = client.embeddings.create(model=MODEL_ID, input=documents)
        doc_embs = [normalize_embedding(item.embedding) for item in doc_resp.data]
    else:
        doc_embs = []
    
    return {
        "query_embedding": query_emb,
        "document_embeddings": doc_embs
    }