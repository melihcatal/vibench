"""
Embed translated segments for translation-memory search using OpenAI.
"""
import os
from typing import List
from openai import OpenAI


def embed_text_segment(text: str) -> List[float]:
    """
    Creates an embedding for a single text segment using OpenAI's API.

    Args:
        text: The text segment to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)
    
    # Normalize input text
    text = text.replace("\\n", " ")

    response = client.embeddings.create(
        input=[text],
        model="text-embedding-3-small"  # Provider-specific model ID
    )
    
    return response.data[0].embedding
