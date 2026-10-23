from embeddings_client import embed_texts


def embed_text(text: str) -> list[float]:
    return embed_texts([text])[0]
