import os
from ibm_watsonx_ai.hlp.embedding import EmbedClient
from translation_models import *


def embed_translated_segments(
    translated_texts: list[str], model_id: str = "text-embedding-3-large"
) -> list[list[float]]:
    """
    Embeds translated segments for translation-memory search.

    Args:
        translated_texts: List of translated strings.
        model_id: Embedding model identifier (watsonx or other provider).

    Returns:
        List of embedding vectors (list of floats) for each segment.
    """
    embed_client = EmbedClient()
    embeddings = []
    for text in translated_texts:
        resp = embed_client.embed(text, model_id=model_id)
        # Assume resp returns a list/ array of floats
        embeddings.append(resp.embedding)
    return embeddings
