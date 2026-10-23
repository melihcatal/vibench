import os
import cohere
from typing import List
from model_models import EmbeddingResult


def embed_texts(texts_to_embed: List[str]) -> EmbeddingResult:
    """
    Generates embeddings for a list of texts using the Cohere API.
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    response = co.embed(
        texts=texts_to_embed, model="embed-english-v3.0", input_type="search_document"
    )

    return EmbeddingResult(embeddings=response.embeddings, raw_result=response)
