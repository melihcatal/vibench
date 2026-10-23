from typing import List, Dict, Tuple
from embeddings_client import get_cohere_client, handle_api_error
from embeddings_models import normalize_embedding


def embed_for_search(query: str, documents: List[str]) -> Tuple[List[float], List[List[float]]]:
    client = get_cohere_client()
    try:
        response = client.embed(
            texts=[query] + documents,
            model="embed-english-v3.0",
            input_type="search_query" if query else "search_document",
            truncate="END",
        )
        embeddings = response.embeddings
        query_embedding = normalize_embedding(embeddings[0])
        doc_embeddings = [normalize_embedding(embedding) for embedding in embeddings[1:]]
        return query_embedding, doc_embeddings
    except Exception as e:
        handle_api_error(e)