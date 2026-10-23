import os
from typing import List
from model_client import get_llm_client


def embed_output(text: str, model: str = "BAAI/bge-small-en-v1.5") -> List[float]:
    """
    Embed model outputs for clustering or retrieval using Hugging Face's Inference API.
    """
    client = get_llm_client()
    response = client.post(
        f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model}",
        json={"inputs": text, "options": {"wait_for_model": True}},
        headers={
            "Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY')}",
            "Content-Type": "application/json"
        }
    )
    response.raise_for_status()
    return response.json()