"""
Embed moderation rationales for case retrieval using OpenAI Embeddings.

Provider: OpenAI Embeddings
SDK: openai
Model: text-embedding-3-small
"""

from typing import List, Optional

import openai

from safety_models import ModerationResponse


def _build_rationale_text(moderation: ModerationResponse) -> str:
    """Construct a human-readable rationale string from a ModerationResponse."""
    parts = [f"Text: {moderation.text}"]
    flagged = [c for c in moderation.categories if c.is_flagged]
    if flagged:
        parts.append("Flagged categories:")
        for cat in flagged:
            parts.append(
                f"  - {cat.category} (severity {cat.severity}, score {cat.score:.2f})"
            )
    else:
        parts.append("No categories flagged.")
    parts.append(f"Overall safe: {moderation.is_safe}")
    return "\n".join(parts)


def embed_moderation_rationale(
    moderation: ModerationResponse,
    api_key: Optional[str] = None,
    model: str = "text-embedding-3-small",
) -> List[float]:
    """
    Generate an embedding vector for a single moderation rationale using
    OpenAI's text-embedding-3-small model.

    Provider: OpenAI Embeddings
    Model: text-embedding-3-small
    """
    client = openai.OpenAI(api_key=api_key)
    rationale = _build_rationale_text(moderation)

    response = client.embeddings.create(
        model=model,
        input=rationale,
    )
    return response.data[0].embedding


def embed_moderation_rationales(
    moderations: List[ModerationResponse],
    api_key: Optional[str] = None,
    model: str = "text-embedding-3-small",
) -> List[List[float]]:
    """
    Generate embedding vectors for a batch of moderation rationales using
    OpenAI's text-embedding-3-small model.

    Provider: OpenAI Embeddings
    Model: text-embedding-3-small
    """
    client = openai.OpenAI(api_key=api_key)

    rationales = [_build_rationale_text(m) for m in moderations]

    response = client.embeddings.create(
        model=model,
        input=rationales,
    )
    sorted_data = sorted(response.data, key=lambda d: d.index)
    return [d.embedding for d in sorted_data]


if __name__ == "__main__":
    from safety_models import CategoryResult, ModerationResponse

    sample = ModerationResponse(
        text="Sample flagged message",
        categories=[
            CategoryResult(category="Violence", severity=5, score=0.571, is_flagged=True),
        ],
        max_severity=5,
        is_safe=False,
    )
    embedding = embed_moderation_rationale(sample)
    print(f"Embedding dimension: {len(embedding)}")
    print(f"First 5 values: {embedding[:5]}")
