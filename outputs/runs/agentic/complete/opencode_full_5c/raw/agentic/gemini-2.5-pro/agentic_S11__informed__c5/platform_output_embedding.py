import os
import cohere
from typing import List

from model_models import EmbeddingResponse


def embed_text(texts_to_embed: List[str]) -> EmbeddingResponse:
    """
    Embeds platform outputs for evaluation or retrieval using Cohere.

    Args:
        texts_to_embed: A list of strings to be embedded.

    Returns:
        An EmbeddingResponse object containing the list of embeddings.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    response = co.embed(
        texts=texts_to_embed, model="embed-english-v3.0", input_type="search_document"
    )

    return EmbeddingResponse(embeddings=response.embeddings)
