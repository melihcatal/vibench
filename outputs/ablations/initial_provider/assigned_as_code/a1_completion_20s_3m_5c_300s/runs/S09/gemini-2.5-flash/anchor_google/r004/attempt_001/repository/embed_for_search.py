import os
from typing import List, Dict, Union
from embeddings_client import EmbeddingsClient
from embeddings_models import GENAI_EMBEDDING_MODEL

def embed_for_search(payload: Dict, config: Dict = None) -> Dict:
    config = config or {}
    client_wrapper = EmbeddingsClient(api_key=config.get("api_key"))
    genai_client = client_wrapper.get_client()

    query_text = payload.get("query")
    document_texts = payload.get("documents", [])

    if not isinstance(query_text, str):
        raise ValueError("Payload must contain a 'query' key with a string.")
    if not isinstance(document_texts, list) or not all(isinstance(d, str) for d in document_texts):
        raise ValueError("Payload must contain a 'documents' key with a list of strings.")

    all_texts_to_embed = [query_text] + document_texts

    if not all_texts_to_embed:
        return {"query_embedding": [], "document_embeddings": []}

    # Use genai.embed_content for all texts
    response = genai_client.embed_content(
        model=GENAI_EMBEDDING_MODEL,
        content=all_texts_to_embed
    )

    # Extract embeddings
    all_embeddings = [list(emb.values) for emb in response.embeddings]

    query_embedding = all_embeddings[0]
    document_embeddings = all_embeddings[1:]

    return {"query_embedding": query_embedding, "document_embeddings": document_embeddings}
