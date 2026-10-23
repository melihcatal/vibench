import os
import cohere
from typing import List

def embed_caption_chunk(caption: str) -> List[float]:
    """
    Embeds a single caption chunk for semantic search using Cohere.
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    try:
        response = co.embed(
            texts=[caption],
            model="embed-english-v3.0",
            input_type="search_document"
        )
        return response.embeddings[0]
    except cohere.CohereError as e:
        print(f"Cohere API error: {e}")
        return []

def embed_multiple_captions(captions: List[str]) -> List[List[float]]:
    """
    Embeds a batch of caption chunks.
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)
    
    try:
        response = co.embed(
            texts=captions,
            model="embed-english-v3.0",
            input_type="search_document"
        )
        return response.embeddings
    except cohere.CohereError as e:
        print(f"Cohere API error: {e}")
        return []
