import os
from typing import List
import openai

def get_embedding(text_chunk: str, model: str = "text-embedding-3-small") -> List[float]:
    """Generates a vector embedding for a caption chunk using OpenAI Embeddings API.

    Args:
        text_chunk: The text content for which to generate an embedding.
        model: The OpenAI embedding model to use (e.g., "text-embedding-3-small", "text-embedding-3-large").

    Returns:
        List[float]: A list of floats representing the embedding vector.
    """
    if not text_chunk.strip():
        return []

    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    try:
        response = client.embeddings.create(
            input=[text_chunk],
            model=model
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"OpenAI embedding error: {e}")
        return []
