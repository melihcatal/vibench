import os
import cohere
from typing import List
from safety_models import EmbeddingResult


def embed_moderation_reason(texts: List[str]) -> EmbeddingResult:
    """
    Embeds moderation rationales for case retrieval using Cohere.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    try:
        response = co.embed(
            texts=texts, model="embed-english-v3.0", input_type="search_document"
        )
        embeddings = response.embeddings
    except cohere.CohereError as e:
        return EmbeddingResult(embeddings=[[float("nan")] * 1024] * len(texts))

    return EmbeddingResult(embeddings=embeddings)
