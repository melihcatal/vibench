"""
[LATER-STEP] moderation_reason_embedding.py
Embed moderation rationales for case retrieval.
Uses the OpenAI Embeddings API (openai SDK, text-embedding-3-small model).
"""

from typing import Optional

from openai import OpenAI

from safety_client import get_openai_client
from safety_models import ModerationResponse


OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def embed_moderation_rationale(
    rationale_text: str,
    api_key: Optional[str] = None,
    model: str = OPENAI_EMBEDDING_MODEL,
) -> list[float]:
    """
    Generate an embedding vector for a moderation rationale text.

    Useful for semantic similarity search to retrieve similar past moderation cases.

    Args:
        rationale_text: The rationale or explanation for the moderation decision.
        api_key: Optional OpenAI API key. Falls back to OPENAI_API_KEY env var.
        model: OpenAI embedding model identifier (default: text-embedding-3-small).

    Returns:
        List of floats representing the embedding vector.
    """
    client = get_openai_client(api_key=api_key)

    response = client.embeddings.create(
        input=rationale_text,
        model=model,
    )

    return response.data[0].embedding


def embed_batch_rationales(
    rationale_texts: list[str],
    api_key: Optional[str] = None,
    model: str = OPENAI_EMBEDDING_MODEL,
    batch_size: int = 100,
) -> list[list[float]]:
    """
    Generate embeddings for multiple moderation rationale texts.

    Args:
        rationale_texts: List of rationale texts to embed.
        api_key: Optional OpenAI API key.
        model: OpenAI embedding model identifier (default: text-embedding-3-small).
        batch_size: Maximum texts per API call (OpenAI limit).

    Returns:
        List of embedding vectors, one per input text.
    """
    client = get_openai_client(api_key=api_key)
    all_embeddings: list[list[float]] = []

    for i in range(0, len(rationale_texts), batch_size):
        chunk = rationale_texts[i : i + batch_size]
        response = client.embeddings.create(input=chunk, model=model)
        for item in response.data:
            all_embeddings.append(item.embedding)

    return all_embeddings


def build_case_embedding(
    text: str,
    response: ModerationResponse,
    reviewer_note: str = "",
    api_key: Optional[str] = None,
    model: str = OPENAI_EMBEDDING_MODEL,
) -> list[float]:
    """
    Build a composite embedding from the original text, moderation result,
    and optional reviewer note for case retrieval.

    Args:
        text: The original moderated text.
        response: ModerationResponse from the moderation call.
        reviewer_note: Optional reviewer annotation.
        api_key: Optional OpenAI API key.
        model: OpenAI embedding model identifier.

    Returns:
        Embedding vector for the combined case information.
    """
    flagged_cats = [
        f"{c.category} (score={c.score:.3f})"
        for c in response.categories
        if c.flagged or c.score > 0.2
    ]

    rationale_parts = [
        f"Content: {text[:300]}",
        f"Moderation: flagged={response.flagged}",
        f"Categories: {', '.join(flagged_cats) or 'none'}",
    ]
    if reviewer_note:
        rationale_parts.append(f"Reviewer note: {reviewer_note}")

    combined_rationale = " | ".join(rationale_parts)
    return embed_moderation_rationale(
        combined_rationale, api_key=api_key, model=model
    )


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """
    Compute cosine similarity between two embedding vectors.

    Args:
        a: First embedding vector.
        b: Second embedding vector.

    Returns:
        Cosine similarity score between 0 and 1.
    """
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(x * x for x in b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)
