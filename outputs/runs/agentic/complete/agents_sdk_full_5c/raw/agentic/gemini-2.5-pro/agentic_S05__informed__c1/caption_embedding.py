import os
import cohere
from typing import List

def embed_caption_chunk(caption_text: str) -> List[float]:
    """
    Embeds a single caption chunk for semantic search using Cohere.

    Args:
        caption_text: The text of the caption chunk.

    Returns:
        A list of floats representing the embedding vector.
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable is not set.")

    co = cohere.Client(api_key)

    try:
        response = co.embed(
            texts=[caption_text],
            model="embed-english-v3.0",
            input_type="search_document"
        )
        return response.embeddings[0]
    except cohere.CohereError as e:
        print(f"An error occurred with the Cohere API: {e}")
        return []
