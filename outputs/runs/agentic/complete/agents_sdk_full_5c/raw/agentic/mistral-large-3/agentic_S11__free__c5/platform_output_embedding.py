import os
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer

def embed_output(text: str, model_name: str = "all-MiniLM-L6-v2") -> Dict[str, Any]:
    """
    Embeds Cohere model output using Sentence Transformers (Hugging Face) for evaluation or retrieval.
    Returns embedding vector and model details.
    """
    model = SentenceTransformer(model_name)
    embedding = model.encode(text, convert_to_tensor=False).tolist()

    return {
        "embedding": embedding,
        "model_name": model_name,
        "dimensions": len(embedding),
    }