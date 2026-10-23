from typing import List
from embeddings_client import get_cohere_client, handle_api_error
from embeddings_models import EmbeddingRequest, normalize_embedding


def embed_batch(texts: List[str]) -> List[List[float]]:
    client = get_cohere_client()
    try:
        response = client.embed(
            texts=texts,
            model="embed-english-v3.0",
            input_type="search_document",
            truncate="END",
        )
        embeddings = response.embeddings
        return [normalize_embedding(embedding) for embedding in embeddings]
    except Exception as e:
        handle_api_error(e)