from typing import List
from embeddings_client import get_embeddings_client, create_embedding
from embeddings_models import parse_embeddings_response

MODEL = "text-embedding-3-small"


def embed_text(text: str) -> List[float]:
    client = get_embeddings_client()
    response = create_embedding(client, MODEL, [text])
    embs = parse_embeddings_response(response)
    return embs[0]
