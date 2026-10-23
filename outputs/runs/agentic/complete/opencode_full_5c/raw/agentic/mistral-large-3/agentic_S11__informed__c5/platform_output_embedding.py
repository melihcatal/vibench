from typing import List, Dict, Any, Optional
import os
import cohere


def embed_with_cohere(
    texts: List[str],
    model: str = "embed-english-v3.0",
    input_type: str = "search_document",
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Embeds platform model outputs using Cohere's embedding API.
    Returns embeddings and metadata for evaluation or retrieval.
    """
    if api_key is None:
        api_key = os.getenv("COHERE_API_KEY")
    if api_key is None:
        raise ValueError("COHERE_API_KEY environment variable not set")

    co = cohere.Client(api_key)
    response = co.embed(
        texts=texts,
        model=model,
        input_type=input_type,
    )

    return {
        "embeddings": response.embeddings,
        "texts": texts,
        "model": model,
        "input_type": input_type,
        "meta": response.meta,
    }
