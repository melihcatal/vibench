from typing import List
from embeddings_client import client
from embeddings_models import MODEL_ID, normalize_embedding

def embed_text(text: str) -> List[float]:
    response = client.embeddings.create(
        model=MODEL_ID,
        input=text
    )
    return normalize_embedding(response.data[0].embedding)