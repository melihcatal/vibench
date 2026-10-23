import os
from openai import OpenAI
from typing import List

def embed_asset_data(text_to_embed: str) -> List[float]:
    """
    Embeds object metadata and extracted text for search using OpenAI's embedding models.

    Args:
        text_to_embed (str): The combined text (metadata + extracted content) to embed.

    Returns:
        List[float]: A list of floats representing the embedding vector.
    """
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=openai_api_key)

    try:
        response = client.embeddings.create(
            input=text_to_embed,
            model="text-embedding-ada-002"  # A common and effective embedding model
        )
        if response.data and response.data[0].embedding:
            return response.data[0].embedding
        else:
            return []
    except Exception as e:
        print(f"An error occurred during embedding generation: {e}")
        return []
