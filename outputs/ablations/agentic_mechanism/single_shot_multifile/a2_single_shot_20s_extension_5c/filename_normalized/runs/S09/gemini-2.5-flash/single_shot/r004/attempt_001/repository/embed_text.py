import os
from typing import List
from embeddings_client import get_openai_embedding_client, OPENAI_EMBEDDING_MODEL

def embed_text(text: str) -> List[float]:
    client = get_openai_embedding_client()
    response = client.embeddings.create(
        input=[text],
        model=OPENAI_EMBEDDING_MODEL
    )
    return response.data[0].embedding
