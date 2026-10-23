import os
import cohere
from typing import List

def embed_text_segment(text: str) -> List[float]:
    """
    Embeds a single translated text segment for translation-memory search.

    Args:
        text: The text segment to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    response = co.embed(
        texts=[text],
        model='embed-english-v3.0',
        input_type='search_document'
    )

    if response.embeddings:
        return response.embeddings[0]
    else:
        return []
