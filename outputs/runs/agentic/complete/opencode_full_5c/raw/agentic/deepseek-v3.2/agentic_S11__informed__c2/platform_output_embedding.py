import os
import openai
from typing import List, Dict, Any
import numpy as np


def get_openai_embedding(
    text: str, model: str = "text-embedding-3-small"
) -> Dict[str, Any]:
    """
    Generate embeddings for platform outputs using OpenAI Embeddings API.
    """
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError(
            "OpenAI API key must be set in OPENAI_API_KEY environment variable"
        )

    client = openai.OpenAI(api_key=api_key)

    try:
        response = client.embeddings.create(
            model=model, input=text, encoding_format="float"
        )

        embedding = response.data[0].embedding
        usage = response.usage

        return {
            "embedding": embedding,
            "model": model,
            "usage": {
                "prompt_tokens": usage.prompt_tokens,
                "total_tokens": usage.total_tokens,
            },
            "dimensions": len(embedding),
        }

    except openai.OpenAIError as e:
        return {
            "embedding": [],
            "error": f"OpenAI embedding error: {str(e)}",
            "model": model,
        }


def batch_embed_texts(
    texts: List[str], model: str = "text-embedding-3-small"
) -> List[Dict[str, Any]]:
    """
    Generate embeddings for multiple texts.
    """
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError(
            "OpenAI API key must be set in OPENAI_API_KEY environment variable"
        )

    client = openai.OpenAI(api_key=api_key)

    try:
        response = client.embeddings.create(
            model=model, input=texts, encoding_format="float"
        )

        results = []
        for i, data in enumerate(response.data):
            results.append({"text": texts[i], "embedding": data.embedding, "index": i})

        return {
            "embeddings": results,
            "model": model,
            "total_tokens": response.usage.total_tokens,
            "dimensions": len(response.data[0].embedding) if response.data else 0,
        }

    except openai.OpenAIError as e:
        return {
            "embeddings": [],
            "error": f"OpenAI batch embedding error: {str(e)}",
            "model": model,
        }


def calculate_similarity(embedding1: List[float], embedding2: List[float]) -> float:
    """
    Calculate cosine similarity between two embeddings.
    """
    if not embedding1 or not embedding2:
        return 0.0

    if len(embedding1) != len(embedding2):
        raise ValueError("Embeddings must have the same dimensions")

    vec1 = np.array(embedding1)
    vec2 = np.array(embedding2)

    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return float(dot_product / (norm1 * norm2))


def embed_for_evaluation(text: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Generate embeddings specifically for evaluation or retrieval purposes.
    """
    embedding_result = get_openai_embedding(text)

    result = {"text": text, "embedding_info": embedding_result}

    if metadata:
        result["metadata"] = metadata

    if "embedding" in embedding_result and embedding_result["embedding"]:
        result["embedding_vector"] = embedding_result["embedding"]
        result["embedding_dimensions"] = len(embedding_result["embedding"])

    return result
