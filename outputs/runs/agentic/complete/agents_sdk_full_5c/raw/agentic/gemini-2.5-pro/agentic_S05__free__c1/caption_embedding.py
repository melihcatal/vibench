import os
from typing import List
import cohere

def embed_caption_chunk(text: str) -> List[float]:
    """
    Embeds a caption chunk for semantic search using the Cohere API.
    
    Requires the COHERE_API_KEY environment variable to be set.

    Args:
        text: The caption text to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    # The Cohere client automatically reads the COHERE_API_KEY from env vars.
    co = cohere.Client(os.getenv("COHERE_API_KEY"))

    response = co.embed(
        texts=[text],
        model="embed-english-v3.0",
        input_type="search_document"
    )
    
    return response.embeddings[0]
