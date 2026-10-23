import numpy as np
from embeddings_client import get_embeddings_client
from embeddings_models import MODEL_NAME, normalize_embedding, cosine_similarity

def similarity_score(text1: str, text2: str) -&gt; float:
    client = get_embeddings_client()
    # Embed text1 as query
    resp1 = client.embed([text1], model=MODEL_NAME, input_type='search_query')
    emb1 = normalize_embedding(resp1.embeddings[0].embedding)
    # Embed text2 as document
    resp2 = client.embed([text2], model=MODEL_NAME, input_type='search_document')
    emb2 = normalize_embedding(resp2.embeddings[0].embedding)
    return cosine_similarity(emb1, emb2)