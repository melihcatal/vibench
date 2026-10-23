import os
from typing import List
import cohere


def get_script_embedding(scripts: List[str]) -> List[List[float]]:
    """
    Embeds narration scripts for voice-asset search using Cohere.

    Args:
        scripts: A list of script strings to embed.

    Returns:
        A list of embedding vectors.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    response = co.embed(
        texts=scripts,
        model="embed-english-v3.0",
        input_type="search_document",
    )

    return response.embeddings
