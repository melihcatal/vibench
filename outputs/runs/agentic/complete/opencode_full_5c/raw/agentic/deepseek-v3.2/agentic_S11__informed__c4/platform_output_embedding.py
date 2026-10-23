import os
import cohere
from typing import List, Dict, Any
import numpy as np


def embed_text(text: str, model: str = "embed-english-v3.0") -> Dict[str, Any]:
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable must be set")

    client = cohere.Client(api_key)

    response = client.embed(texts=[text], model=model, input_type="search_document")

    embedding = response.embeddings[0]

    return {
        "text": text,
        "embedding": embedding,
        "model": model,
        "provider": "Cohere",
        "embedding_dimensions": len(embedding),
        "request_id": response.id if hasattr(response, "id") else None,
    }


def batch_embed_texts(
    texts: List[str],
    model: str = "embed-english-v3.0",
    input_type: str = "search_document",
) -> List[Dict[str, Any]]:
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable must be set")

    client = cohere.Client(api_key)

    response = client.embed(texts=texts, model=model, input_type=input_type)

    results = []
    for i, embedding in enumerate(response.embeddings):
        result = {
            "text": texts[i],
            "embedding": embedding,
            "model": model,
            "input_type": input_type,
            "provider": "Cohere",
            "embedding_dimensions": len(embedding),
        }
        results.append(result)

    return results


def compute_similarity(embedding1: List[float], embedding2: List[float]) -> float:
    vec1 = np.array(embedding1)
    vec2 = np.array(embedding2)

    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    similarity = dot_product / (norm1 * norm2)
    return float(similarity)


def embed_with_metadata(
    text: str, metadata: Dict[str, Any] = None, model: str = "embed-english-v3.0"
) -> Dict[str, Any]:
    embedding_result = embed_text(text, model)

    if metadata:
        embedding_result["metadata"] = metadata

    return embedding_result


def get_available_embedding_models() -> List[Dict[str, Any]]:
    cohere_models = [
        {
            "id": "embed-english-v3.0",
            "name": "Cohere Embed English v3.0",
            "dimensions": 1024,
        },
        {
            "id": "embed-multilingual-v3.0",
            "name": "Cohere Embed Multilingual v3.0",
            "dimensions": 1024,
        },
        {
            "id": "embed-english-light-v3.0",
            "name": "Cohere Embed English Light v3.0",
            "dimensions": 384,
        },
        {
            "id": "embed-multilingual-light-v3.0",
            "name": "Cohere Embed Multilingual Light v3.0",
            "dimensions": 384,
        },
    ]

    return cohere_models
