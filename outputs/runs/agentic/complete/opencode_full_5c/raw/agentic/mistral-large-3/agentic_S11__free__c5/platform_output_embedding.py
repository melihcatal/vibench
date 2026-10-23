from typing import Dict, Any, List
from model_models import ChatResponse
from sentence_transformers import SentenceTransformer


def platform_output_embedding(response: ChatResponse) -> Dict[str, Any]:
    """
    Embeds Azure AI Inference model output using Sentence Transformers.
    Uses "all-MiniLM-L6-v2" as the concrete model identifier.
    """
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embedding = model.encode(response.content)

    return {
        "embedding": embedding.tolist(),
        "model": "all-MiniLM-L6-v2",
        "dimensions": len(embedding),
    }
