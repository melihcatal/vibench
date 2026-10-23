import os
from openai import OpenAI

def embed_caption_chunk(text_chunk: str, model="text-embedding-3-small"):
    """
    Creates a vector embedding for a caption chunk using OpenAI's API.

    Args:
        text_chunk: The text content to embed.
        model: The OpenAI embedding model to use.

    Returns:
        A list of floats representing the embedding vector.
    """
    # The OpenAI client looks for the OPENAI_API_KEY environment variable by default.
    try:
        client = OpenAI()
    except Exception as e:
        raise RuntimeError("Could not initialize OpenAI client. Ensure OPENAI_API_KEY is set.") from e

    if not text_chunk or not text_chunk.strip():
        return []

    text_chunk = text_chunk.replace("\n", " ")

    response = client.embeddings.create(input=[text_chunk], model=model)
    
    return response.data[0].embedding
