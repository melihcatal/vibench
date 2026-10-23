from typing import List
from embeddings_client import get_openai_client
from embeddings_models import Embedding, normalize_embedding


def embed_text(text: str, model: str = "text-embedding-3-small") -> Embedding:
    client = get_openai_client()
    response = client.embeddings.create(model=model, input=text.strip())
    return normalize_embedding(response.data[0].embedding)
