import os
import cohere
from typing import List


def embed_script(script_texts: List[str]) -> List[List[float]]:
    """
    Embeds narration scripts for voice-asset search using Cohere.

    Args:
        script_texts: A list of narration scripts to embed.

    Returns:
        A list of embedding vectors.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    response = co.embed(
        texts=script_texts, model="embed-english-v3.0", input_type="search_document"
    )

    return response.embeddings
