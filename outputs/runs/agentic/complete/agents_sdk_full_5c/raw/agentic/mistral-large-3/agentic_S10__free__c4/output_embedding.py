import os
from typing import List, Optional
from model_client import get_llm_client


def embed_output(text: str, model: Optional[str] = "text-embedding-3-small") -> List[float]:
    """
    Embed model outputs for clustering or retrieval using OpenAI's embedding API.
    """
    client = get_llm_client()
    response = client.embeddings.create(
        input=text,
        model=model
    )
    return response.data[0].embedding