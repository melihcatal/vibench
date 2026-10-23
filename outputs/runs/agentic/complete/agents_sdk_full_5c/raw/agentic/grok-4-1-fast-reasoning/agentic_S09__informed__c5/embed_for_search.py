import numpy as np
from embeddings_client import get_embeddings_client
from embeddings_models import MODEL_NAME, normalize_embedding

def embed_for_search(query: str, documents: list[str]) -&gt; tuple[list[float], list[list[float]]]:
    client = get_embeddings_client()
    # Embed query
    q_resp = client.embed([query], model=MODEL_NAME, input_type='search_query')
    query_emb = normalize_embedding(q_resp.embeddings[0].embedding).tolist()
    # Embed documents
    d_resp = client.embed(documents, model=MODEL_NAME, input_type='search_document')
    doc_embs = [normalize_embedding(e.embedding).tolist() for e in d_resp.embeddings]
    return query_emb, doc_embs