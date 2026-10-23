from typing import List
from embeddings_client import get_embeddings_client
from embeddings_models import normalize_texts


def embed_text(text: str) -> List[float]:
    client = get_embeddings_client()
    response = client.embeddings.create(
        model="text-embedding-3-small", input=normalize_texts([text])
    )
    return [float(x) for x in response.data[0].embedding]
