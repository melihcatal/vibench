from __future__ import annotations

from embeddings_client import embed_texts


def generate_embeddings(texts: list[str]) -> list[list[float]]:
    return embed_texts(texts).embeddings
