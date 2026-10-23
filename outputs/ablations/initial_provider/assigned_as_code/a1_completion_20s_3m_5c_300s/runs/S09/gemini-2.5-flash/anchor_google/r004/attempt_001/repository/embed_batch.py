import os
from typing import List, Dict
from embeddings_client import EmbeddingsClient
from embeddings_models import GENAI_EMBEDDING_MODEL

def embed_batch(payload: Dict, config: Dict = None) -> Dict:
    config = config or {}
    client_wrapper = EmbeddingsClient(api_key=config.get("api_key"))
    genai_client = client_wrapper.get_client()

    texts = payload.get("texts", [])
    if not isinstance(texts, list) or not all(isinstance(t, str) for t in texts):
        raise ValueError("Payload must contain a 'texts' key with a list of strings.")

    # The genai.embed_content function takes a list of texts directly.
    # Using the same model as embed_text.py for consistency.
    response = genai_client.embed_content(
        model=GENAI_EMBEDDING_MODEL,
        content=texts
    )

    # The response.embeddings will be a list of Embedding objects. Extract their values.
    embeddings = [list(emb.values) for emb in response.embeddings]
    return {"embeddings": embeddings}
