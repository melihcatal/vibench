import os
from openai import OpenAI

def embed_caption_chunk(caption_chunk: str):
    """
    Embeds a caption chunk using OpenAI's text-embedding-ada-002 model.

    Args:
        caption_chunk: The text chunk to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    # Ensure the OpenAI API key is set as an environment variable
    # For example: export OPENAI_API_KEY='sk-your-key'
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)

    response = client.embeddings.create(
        input=caption_chunk,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding
