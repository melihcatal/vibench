from typing import List, Dict, Any
from model_client import get_model_client

def embed_output(text: str, model_identifier: str = "embed-english-v3.0") -> Dict[str, Any]:
    """
    Embeds Cohere model outputs for evaluation or retrieval using Cohere Embeddings.
    Returns embedding vector and metadata.
    """
    client = get_model_client()
    response = client.client.embed(
        texts=[text],
        model=model_identifier,
        input_type="search_document",
    )

    return {
        "embedding": response.embeddings[0],
        "model": model_identifier,
        "provider": "cohere",
    }