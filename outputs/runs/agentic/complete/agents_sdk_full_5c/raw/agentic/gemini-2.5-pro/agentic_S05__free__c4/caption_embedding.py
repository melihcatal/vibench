import os
from openai import OpenAI

def embed_caption_chunk(text_chunk: str):
    """
    Creates a vector embedding for a caption chunk using OpenAI's API.

    Args:
        text_chunk: The text to embed.

    Returns:
        A list of floats representing the embedding, or None on error.
    """
    # The OpenAI client looks for OPENAI_API_KEY in the environment by default.
    try:
        client = OpenAI()
        response = client.embeddings.create(
            input=text_chunk,
            model="text-embedding-3-small"  # A specific, cost-effective embedding model
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"An error occurred with the OpenAI API: {e}")
        return None
