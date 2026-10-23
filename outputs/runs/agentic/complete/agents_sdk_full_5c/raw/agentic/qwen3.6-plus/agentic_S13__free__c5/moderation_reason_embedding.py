"""
[LATER-STEP] moderation_reason_embedding.py
Embed moderation rationales for case retrieval using OpenAI embeddings.
Provider: OpenAI — model identifier: text-embedding-3-small
API hostname: api.openai.com
"""

from typing import Optional, Dict, Any, List
import json

from safety_client import get_openai_client, load_safety_config
from safety_models import ModerationEmbedding

DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"


def embed_rationale(
    rationale_text: str,
    model: str = DEFAULT_EMBEDDING_MODEL,
    config: Optional[Dict[str, Any]] = None,
) -> ModerationEmbedding:
    """
    Embed a moderation rationale string using OpenAI's text-embedding-3-small model
    for semantic case retrieval.
    """
    if config is None:
        config = load_safety_config()

    client = get_openai_client(config)

    response = client.embeddings.create(
        input=rationale_text,
        model=model,
    )

    embedding_data = response.data[0]
    embedding_vector = embedding_data.embedding

    return ModerationEmbedding(
        rationale_text=rationale_text,
        embedding=embedding_vector,
        model=model,
        dimension=len(embedding_vector),
    )


def embed_rationales_batch(
    rationales: List[str],
    model: str = DEFAULT_EMBEDDING_MODEL,
    config: Optional[Dict[str, Any]] = None,
) -> List[ModerationEmbedding]:
    """
    Embed multiple moderation rationales in a single batch call
    using OpenAI's text-embedding-3-small model.
    """
    if config is None:
        config = load_safety_config()

    client = get_openai_client(config)

    response = client.embeddings.create(
        input=rationales,
        model=model,
    )

    results = []
    for i, emb_data in enumerate(response.data):
        embedding = ModerationEmbedding(
            rationale_text=rationales[i],
            embedding=emb_data.embedding,
            model=model,
            dimension=len(emb_data.embedding),
        )
        results.append(embedding)

    return results


def embed_rationale_dict(
    rationale_text: str,
    model: str = DEFAULT_EMBEDDING_MODEL,
    config: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Embed a rationale and return as a dict."""
    result = embed_rationale(rationale_text, model=model, config=config)
    return result.to_dict()


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """Compute cosine similarity between two embedding vectors."""
    import math
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)


if __name__ == "__main__":
    rationale = "Content was blocked due to high violence score (0.92) in the violence_graphic category. User has prior violations."
    result = embed_rationale_dict(rationale)
    print(f"Model: {result['model']}, Dimension: {result['dimension']}")
