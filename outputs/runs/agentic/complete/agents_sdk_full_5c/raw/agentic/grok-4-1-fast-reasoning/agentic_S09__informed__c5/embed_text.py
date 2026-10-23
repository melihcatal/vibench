import numpy as np
from embeddings_client import get_embeddings_client
from embeddings_models import MODEL_NAME, normalize_embedding

def embed_text(text: str) -&gt; list[float]:
    client = get_embeddings_client()
    response = client.embed(
        texts=[text],
        model=MODEL_NAME,
        input_type='search_query'
    )
    embedding = response.embeddings[0].embedding
    normalized = normalize_embedding(embedding).tolist()
    return normalized