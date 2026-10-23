from typing import Dict, Any, List
import numpy as np
from sentence_transformers import SentenceTransformer

from .model_models import ChatResponse


def platform_output_embedding(response: ChatResponse) -> Dict[str, Any]:
    """
    Embeds Azure AI Inference model output for evaluation or retrieval using SentenceTransformers.
    Uses the 'all-MiniLM-L6-v2' model for embedding generation.
    """
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embedding = model.encode(response.content, convert_to_numpy=True)

    return {
        "embedding": embedding.tolist(),
        "model": "all-MiniLM-L6-v2",
        "provider": "sentence_transformers",
    }
