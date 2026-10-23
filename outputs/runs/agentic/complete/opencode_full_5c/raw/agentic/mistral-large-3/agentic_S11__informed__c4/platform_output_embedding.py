from typing import Dict, Any, List
import cohere
import os


def platform_output_embedding(text: str) -> Dict[str, Any]:
    """
    Embeds watsonx.ai model output using Cohere Embed API.
    Requires COHERE_API_KEY environment variable.
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY must be set.")

    co = cohere.Client(api_key)
    response = co.embed(texts=[text], model="embed-english-v3.0")

    return {
        "embeddings": response.embeddings,
        "model": "embed-english-v3.0",
        "provider": "Cohere",
    }
