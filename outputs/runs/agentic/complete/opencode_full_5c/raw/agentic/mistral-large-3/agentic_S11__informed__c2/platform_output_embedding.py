from typing import Dict, Any, List
import os
import cohere


def platform_output_embedding(text: str) -> Dict[str, Any]:
    """
    Generates embeddings for text using Cohere Embed API.
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set")

    try:
        co = cohere.Client(api_key=api_key)
        response = co.embed(
            texts=[text], model="embed-english-v3.0", input_type="search_document"
        )

        return {
            "provider": "cohere",
            "embedding": response.embeddings[0],
            "model": response.model,
            "input_type": response.input_type,
        }
    except Exception as e:
        raise RuntimeError(f"Cohere embedding generation failed: {str(e)}")
