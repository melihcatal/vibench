"""
Compute cosine similarity between two embedded texts.

Provider: OpenAI Embeddings API (https://api.openai.com)
Model: text-embedding-3-small
"""

from typing import Optional

from embeddings_client import (
    get_openai_client,
    load_embeddings_config,
    build_embeddings_payload,
    parse_embeddings_response,
)
from embeddings_models import (
    EmbeddingRequest,
    EmbeddingResponse,
    SimilarityResult,
    cosine_similarity,
)


def similarity_score(
    text_a: str,
    text_b: str,
    model: Optional[str] = None,
    dimensions: Optional[int] = None,
    api_key: Optional[str] = None,
) -> SimilarityResult:
    """
    Compute cosine similarity between two texts using OpenAI embeddings.

    Embeds both texts with the OpenAI API and calculates the cosine
    similarity between their embedding vectors.

    Args:
        text_a: First text string
        text_b: Second text string
        model: OpenAI embedding model (default: text-embedding-3-small)
        dimensions: Optional embedding dimensionality
        api_key: OpenAI API key (falls back to OPENAI_API_KEY env var)

    Returns:
        SimilarityResult with score in range [-1, 1]

    Raises:
        ValueError: If either text is empty
        openai.APIError: If the OpenAI API request fails
    """
    if not text_a or not text_a.strip():
        raise ValueError("text_a cannot be empty")
    if not text_b or not text_b.strip():
        raise ValueError("text_b cannot be empty")

    config = load_embeddings_config()
    target_model = model or config["model"]
    target_dimensions = dimensions or config["dimensions"]

    request = EmbeddingRequest(
        texts=[text_a, text_b],
        model=target_model,
        dimensions=target_dimensions,
    )
    request.validate()

    client = get_openai_client(api_key=api_key)
    payload = build_embeddings_payload(
        texts=[text_a, text_b],
        model=target_model,
        dimensions=target_dimensions,
    )

    response = client.embeddings.create(**payload)
    embeddings = parse_embeddings_response(response)

    if len(embeddings) != 2:
        raise ValueError("Expected exactly 2 embeddings from OpenAI API")

    emb_a = embeddings[0]
    emb_b = embeddings[1]
    score = cosine_similarity(emb_a, emb_b)

    result = EmbeddingResponse(
        embeddings=embeddings,
        model=response.model,
        usage={
            "prompt_tokens": response.usage.prompt_tokens,
            "total_tokens": response.usage.total_tokens,
        },
    )

    return SimilarityResult(
        score=score,
        text_a=text_a,
        text_b=text_b,
    )


if __name__ == "__main__":
    import json

    text_1 = "The cat sat on the mat."
    text_2 = "A feline rested on the rug."
    result = similarity_score(text_1, text_2)
    print(json.dumps({
        "text_a": result.text_a,
        "text_b": result.text_b,
        "cosine_similarity": result.score,
        "model": "text-embedding-3-small",
    }, indent=2))
