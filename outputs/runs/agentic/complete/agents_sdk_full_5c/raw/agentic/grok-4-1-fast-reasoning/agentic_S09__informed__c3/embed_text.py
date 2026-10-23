from typing import List
from embeddings_client import get_client, EMBEDDING_MODEL
from embeddings_models import extract_embeddings

def embed_text(text: str) -> List[float]:
    client = get_client()
    response = client.embeddings.create(
        input=[text],
        model=EMBEDDING_MODEL
    )
    embeddings = extract_embeddings(response)
    return embeddings[0]