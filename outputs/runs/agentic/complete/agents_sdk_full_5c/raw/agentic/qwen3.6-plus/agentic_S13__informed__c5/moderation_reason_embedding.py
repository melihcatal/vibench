"""
Embed moderation rationales for case retrieval using hosted embeddings API.
Provider: OpenAI Embeddings via openai SDK.
Model: text-embedding-3-small
Auth: OPENAI_API_KEY
"""

import os
import json
from typing import Optional, List, Dict

from openai import OpenAI


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")


def embed_moderation_reason(
    rationale_text: str,
    model: str = "text-embedding-3-small",
    api_key: Optional[str] = None,
) -> Dict:
    """
    Embed a moderation rationale for case retrieval using OpenAI Embeddings API.

    Args:
        rationale_text: The moderation reason/rationale text to embed.
        model: OpenAI embedding model identifier (default: text-embedding-3-small).
        api_key: Optional OpenAI API key override.

    Returns:
        Dictionary with embedding vector, model info, and input text.
    """
    key = api_key or OPENAI_API_KEY
    if not key:
        raise ValueError("OPENAI_API_KEY is required for OpenAI Embeddings API access.")

    client = OpenAI(api_key=key)

    response = client.embeddings.create(
        input=rationale_text,
        model=model,
    )

    embedding = response.data[0].embedding

    return {
        "input_text": rationale_text,
        "embedding": embedding,
        "dimensions": len(embedding),
        "model": model,
        "provider": "OpenAI Embeddings",
    }


def embed_moderation_reasons_batch(
    rationale_texts: List[str],
    model: str = "text-embedding-3-small",
    api_key: Optional[str] = None,
) -> Dict:
    """
    Embed multiple moderation rationales for case retrieval using OpenAI Embeddings API.

    Args:
        rationale_texts: List of moderation rationale texts to embed.
        model: OpenAI embedding model identifier.
        api_key: Optional OpenAI API key override.

    Returns:
        Dictionary with all embeddings, metadata, and provider info.
    """
    key = api_key or OPENAI_API_KEY
    if not key:
        raise ValueError("OPENAI_API_KEY is required for OpenAI Embeddings API access.")

    client = OpenAI(api_key=key)

    response = client.embeddings.create(
        input=rationale_texts,
        model=model,
    )

    embeddings = []
    for item in response.data:
        embeddings.append({
            "input_text": item.index if item.index < len(rationale_texts) else "",
            "embedding": item.embedding,
            "dimensions": len(item.embedding),
        })

    # Associate input texts with embeddings by index
    for i, emb in enumerate(embeddings):
        if i < len(rationale_texts):
            emb["input_text"] = rationale_texts[i]

    return {
        "embeddings": embeddings,
        "total_count": len(rationale_texts),
        "model": model,
        "provider": "OpenAI Embeddings",
    }


if __name__ == "__main__":
    sample = "Content flagged for hate speech: user targeted a protected group with dehumanizing language."
    result = embed_moderation_reason(sample)
    output = {k: v for k, v in result.items() if k != "embedding"}
    output["embedding_preview"] = result["embedding"][:5]
    print(json.dumps(output, indent=2))
