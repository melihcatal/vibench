import os
import cohere
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class EmbeddingResult:
    embedding: List[float]
    model: str
    raw_response: Optional[Dict] = None


def embed_platform_output(
    text: str, model: str = "embed-english-v3.0"
) -> EmbeddingResult:
    """
    Embed platform outputs for evaluation or retrieval using Cohere Embed API.
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable is required")

    try:
        co = cohere.Client(api_key)

        response = co.embed(texts=[text], model=model, input_type="search_document")

        return EmbeddingResult(
            embedding=response.embeddings[0], model=model, raw_response=response
        )
    except Exception as e:
        raise RuntimeError(f"Failed to generate embeddings with Cohere: {e}")


def embed_batch_platform_outputs(
    texts: List[str], model: str = "embed-english-v3.0"
) -> List[EmbeddingResult]:
    """
    Embed multiple platform outputs in batch.
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable is required")

    try:
        co = cohere.Client(api_key)

        response = co.embed(texts=texts, model=model, input_type="search_document")

        results = []
        for i, embedding in enumerate(response.embeddings):
            results.append(
                EmbeddingResult(embedding=embedding, model=model, raw_response=response)
            )

        return results
    except Exception as e:
        raise RuntimeError(f"Failed to generate batch embeddings with Cohere: {e}")
