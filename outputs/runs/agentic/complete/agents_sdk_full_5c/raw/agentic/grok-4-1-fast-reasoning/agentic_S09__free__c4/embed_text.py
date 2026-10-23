from embeddings_client import get_client
from embeddings_models import normalize_embedding
import numpy as np
from typing import List

EMBEDDING_MODEL = "text-embedding-3-small"

def embed_text(text: str) -> List[float]:
    client = get_client()
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )
    embedding = np.array(response.data[0].embedding)
    return normalize_embedding(embedding).tolist()