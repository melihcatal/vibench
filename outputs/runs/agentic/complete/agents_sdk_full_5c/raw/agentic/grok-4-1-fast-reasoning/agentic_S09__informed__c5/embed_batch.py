import numpy as np
from embeddings_client import get_embeddings_client
from embeddings_models import MODEL_NAME, normalize_embedding

def embed_batch(texts: list[str]) -&gt; list[list[float]]:
    client = get_embeddings_client()
    response = client.embed(
        texts=texts,
        model=MODEL_NAME,
        input_type='search_document'
    )
    normalized_embeddings = [
        normalize_embedding(emb.embedding).tolist()
        for emb in response.embeddings
    ]
    return normalized_embeddings