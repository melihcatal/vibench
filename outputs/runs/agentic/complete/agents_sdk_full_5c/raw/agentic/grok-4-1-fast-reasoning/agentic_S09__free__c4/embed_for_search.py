from embeddings_client import get_client
from embeddings_models import normalize_embedding, cosine_similarity
import numpy as np
from typing import List, Dict, Any

EMBEDDING_MODEL = "text-embedding-3-small"

def embed_for_search(query: str, documents: List[str]) -> Dict[str, Any]:
    client = get_client()
    q_response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=query
    )
    q_emb = np.array(q_response.data[0].embedding)
    d_response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=documents
    )
    d_embs = [np.array(data.embedding) for data in d_response.data]
    scores = [cosine_similarity(q_emb, de) for de in d_embs]
    return {
        "query_embedding": normalize_embedding(q_emb).tolist(),
        "document_embeddings": [normalize_embedding(de).tolist() for de in d_embs],
        "similarity_scores": scores
    }