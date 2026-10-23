"""
Same-scenario: Compute cosine similarity between two embedded texts.
Provider: OpenAI Embeddings API via openai SDK.
Auth: OPENAI_API_KEY
Model: text-embedding-3-small
"""

from typing import Optional

from embeddings_client import create_embeddings_client, DEFAULT_EMBEDDING_MODEL
from embeddings_models import EmbeddingRequest, cosine_similarity, parse_openai_embedding_response


def similarity_score(
    text_a: str,
    text_b: str,
    model: Optional[str] = None,
    dimensions: Optional[int] = None,
    api_key: Optional[str] = None,
) -> float:
    """Compute cosine similarity between the embeddings of two texts using OpenAI.

    Args:
        text_a: First text string.
        text_b: Second text string.
        model: OpenAI embedding model identifier.
        dimensions: Optional output dimensionality.
        api_key: Optional override for OPENAI_API_KEY.

    Returns:
        Cosine similarity score between -1.0 and 1.0.
    """
    resolved_model = model or DEFAULT_EMBEDDING_MODEL
    client = create_embeddings_client(api_key=api_key)

    request_kwargs = {
        "input": [text_a, text_b],
        "model": resolved_model,
        "encoding_format": "float",
    }
    if dimensions is not None:
        request_kwargs["dimensions"] = dimensions

    raw_response = client.embeddings.create(**request_kwargs)

    resp_a = parse_openai_embedding_response(raw_response, index=0)
    resp_b = parse_openai_embedding_response(raw_response, index=1)

    return cosine_similarity(resp_a.embedding, resp_b.embedding)


if __name__ == "__main__":
    s = similarity_score("I love programming in Python.", "Python is my favorite programming language.")
    print(f"Cosine similarity: {s:.4f}")
