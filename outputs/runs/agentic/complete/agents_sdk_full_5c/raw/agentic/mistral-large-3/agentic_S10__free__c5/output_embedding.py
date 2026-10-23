import os
from typing import List
from model_client import get_llm_client


def embed_output(text: str, model: str = "text-embedding-ada-002") -> List[float]:
    """
    Embed model outputs for clustering or retrieval using OpenAI's Embedding API.
    """
    client = get_llm_client()
    response = client.post(
        "https://api.openai.com/v1/embeddings",
        json={
            "input": text,
            "model": model
        },
        headers={
            "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
            "Content-Type": "application/json"
        }
    )
    response.raise_for_status()
    return response.json()["data"][0]["embedding"]