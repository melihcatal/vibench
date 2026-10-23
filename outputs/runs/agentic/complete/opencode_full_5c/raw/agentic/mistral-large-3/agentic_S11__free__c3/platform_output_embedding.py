from typing import Dict, Any, List
import numpy as np
import requests
from sentence_transformers import SentenceTransformer
from .model_client import get_model_client_config
from .model_models import ChatResponse


def platform_output_embedding(
    response: ChatResponse,
    model_name: str = "all-MiniLM-L6-v2",
) -> Dict[str, Any]:
    """
    Embeds Azure AI Inference model output using Sentence Transformers.
    """
    try:
        model = SentenceTransformer(model_name)
    except Exception as e:
        raise ValueError(f"Failed to load embedding model: {e}")

    embedding = model.encode(response.content, convert_to_numpy=True)

    return {
        "embedding": embedding.tolist(),
        "model": model_name,
        "dimensions": len(embedding),
    }
