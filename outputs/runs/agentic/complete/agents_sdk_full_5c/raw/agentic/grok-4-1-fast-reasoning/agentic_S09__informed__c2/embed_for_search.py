from typing import List, Tuple
from embeddings_client import get_client
from embeddings_models import create_request, normalize_embedding

def embed_for_search(query: str, documents: List[str]) -> Tuple[List[float], List[List[float]]]:
    client = get_client()
    q_response = client.embeddings.create(**create_request(query))
    q_emb = normalize_embedding(q_response.data[0].embedding).tolist()
    d_response = client.embeddings.create(**create_request(documents))
    d_embs = [normalize_embedding(data.embedding).tolist() for data in d_response.data]
    return q_emb, d_embs
