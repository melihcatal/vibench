import os
from typing import List
from openai import OpenAI

def get_embedding(text: str) -> List[float]:
    """
    Generates a vector embedding for a text segment using OpenAI.

    Args:
        text: The text segment to embed.

    Returns:
        A list of floats representing the vector embedding.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    
    client = OpenAI(api_key=api_key)
    
    text_to_embed = text.replace("\n", " ")
    
    response = client.embeddings.create(
        input=[text_to_embed],
        model="text-embedding-3-small"
    )
    
    return response.data[0].embedding
