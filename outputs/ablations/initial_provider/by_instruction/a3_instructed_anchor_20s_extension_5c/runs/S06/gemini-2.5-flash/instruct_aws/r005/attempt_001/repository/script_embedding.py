from openai import OpenAI
import os
from typing import List

def script_embedding(text: str, model: str = "text-embedding-ada-002") -> List[float]:
    """
    Embeds narration scripts for voice-asset search using OpenAI Embeddings.

    Args:
        text: The narration script text to embed.
        model: The OpenAI embedding model to use (e.g., "text-embedding-ada-002").

    Returns:
        A list of floats representing the embedding vector.
    """
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY")
    )

    response = client.embeddings.create(
        input=[text],
        model=model
    )

    return response.data[0].embedding
