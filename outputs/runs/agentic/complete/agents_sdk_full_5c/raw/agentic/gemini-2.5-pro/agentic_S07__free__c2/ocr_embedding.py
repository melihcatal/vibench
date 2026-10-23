
import os
from typing import List
from openai import OpenAI

def get_text_embedding(text: str) -> List[float]:
    """
    Generates a vector embedding for a given text using OpenAI's API.

    Requires the OPENAI_API_KEY environment variable to be set.

    Args:
        text: The input string to embed.

    Returns:
        A list of floats representing the vector embedding.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)
    
    # Replace newlines to avoid issues with some models
    text = text.replace("\\n", " ")

    response = client.embeddings.create(
        input=[text],
        model="text-embedding-3-small"
    )

    return response.data[0].embedding
