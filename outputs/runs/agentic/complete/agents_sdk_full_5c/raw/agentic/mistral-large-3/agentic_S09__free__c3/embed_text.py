from typing import List
from embeddings_client import get_cohere_client, handle_api_error
from embeddings_models import EmbeddingRequest, normalize_embedding


def embed_text(text: str) -> List[float]:
    client = get_cohere_client()
    try:
        response = client.embed(
            texts=[text],
            model="embed-english-v3.0",
            input_type="search_document",
            truncate="END",
        )
        embedding = response.embeddings[0]
        return normalize_embedding(embedding)
    except Exception as e:
        handle_api_error(e)