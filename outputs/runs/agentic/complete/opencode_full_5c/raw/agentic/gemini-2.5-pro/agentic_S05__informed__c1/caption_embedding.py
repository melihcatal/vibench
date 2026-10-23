import os
from typing import List
import cohere


def embed_caption_chunk(text: str) -> List[float]:
    """
    Embed a single caption chunk for semantic meeting search using Cohere.
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set")

    co = cohere.Client(api_key)

    try:
        response = co.embed(
            texts=[text], model="embed-english-v3.0", input_type="search_document"
        )
        return response.embeddings[0]
    except cohere.core.api_error.ApiError as e:
        print(f"Error calling Cohere API: {e}")
        return []


def embed_caption_chunks(texts: List[str]) -> List[List[float]]:
    """
    Embed multiple caption chunks in a single call using Cohere.
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set")

    co = cohere.Client(api_key)

    try:
        response = co.embed(
            texts=texts, model="embed-english-v3.0", input_type="search_document"
        )
        return response.embeddings
    except cohere.core.api_error.ApiError as e:
        print(f"Error calling Cohere API: {e}")
        return [[] for _ in texts]
