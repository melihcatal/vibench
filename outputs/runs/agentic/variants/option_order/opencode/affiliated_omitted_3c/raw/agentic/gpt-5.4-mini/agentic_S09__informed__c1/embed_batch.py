from embeddings_client import embed_texts


def embed_batch(texts: list[str]) -> list[list[float]]:
    return embed_texts(texts)
