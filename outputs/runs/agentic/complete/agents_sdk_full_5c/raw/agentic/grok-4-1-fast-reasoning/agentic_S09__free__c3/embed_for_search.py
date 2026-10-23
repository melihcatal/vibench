from typing import List, Tuple
from embeddings_client import get_client
from embeddings_models import MODEL_EMBED, normalize_text, normalize_texts

def embed_for_search(query: str, documents: List[str]) -> Tuple[List[float], List[List[float]]]:
    client = get_client()
    query_emb_response = client.embeddings.create(
        model=MODEL_EMBED,
        input=normalize_text(query)
    )
    query_emb = query_emb_response.data[0].embedding
    docs_response = client.embeddings.create(
        model=MODEL_EMBED,
        input=normalize_texts(documents)
    )
    docs_embs = [data.embedding for data in docs_response.data]
    return query_emb, docs_embs