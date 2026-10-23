"""Embed moderation rationales for case retrieval using OpenAI text-embedding-3-small."""

import os
from typing import Dict, List

from openai import OpenAI


def embed_moderation_rationale(
    rationale: str,
    model: str = "text-embedding-3-small",
) -> Dict[str, object]:
    """Generate an embedding vector for a moderation rationale to support case retrieval.

    Uses OpenAI's text-embedding-3-small model via api.openai.com to produce a dense
    vector representation of a moderation rationale, enabling semantic similarity search
    across moderation cases.

    Args:
        rationale: The moderation rationale text to embed.
        model: OpenAI embedding model (default: text-embedding-3-small).

    Returns:
        Dict with 'embedding' (list of floats), 'model', 'dimensions', and 'provider'.
    """
    api_key = os.environ.get("OPENAI_API_KEY", "")
    client = OpenAI(api_key=api_key)

    response = client.embeddings.create(
        model=model,
        input=rationale,
    )

    embedding_data = response.data[0]
    return {
        "embedding": embedding_data.embedding,
        "model": model,
        "dimensions": len(embedding_data.embedding),
        "provider": "openai",
        "provider_endpoint": "api.openai.com",
    }


def embed_batch_rationales(
    rationales: List[str],
    model: str = "text-embedding-3-small",
) -> List[Dict[str, object]]:
    """Generate embedding vectors for multiple moderation rationales.

    Uses OpenAI's text-embedding-3-small model on api.openai.com.

    Args:
        rationales: List of rationale strings to embed.
        model: OpenAI embedding model (default: text-embedding-3-small).

    Returns:
        List of dicts, each containing 'embedding', 'model', 'dimensions', and 'index'.
    """
    api_key = os.environ.get("OPENAI_API_KEY", "")
    client = OpenAI(api_key=api_key)

    response = client.embeddings.create(
        model=model,
        input=rationales,
    )

    results = []
    for item in response.data:
        results.append({
            "index": item.index,
            "embedding": item.embedding,
            "model": model,
            "dimensions": len(item.embedding),
            "provider": "openai",
            "provider_endpoint": "api.openai.com",
        })

    return results


if __name__ == "__main__":
    sample_rationale = "Content flagged for hate speech due to derogatory language targeting a protected group."
    result = embed_moderation_rationale(sample_rationale)
    print(f"Model: {result['model']}, Dimensions: {result['dimensions']}, Provider: {result['provider']}")
