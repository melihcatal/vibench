from __future__ import annotations

from embeddings_client import embed_texts


def generate_embedding(text: str) -> list[float]:
    return embed_texts([text]).embeddings[0]
