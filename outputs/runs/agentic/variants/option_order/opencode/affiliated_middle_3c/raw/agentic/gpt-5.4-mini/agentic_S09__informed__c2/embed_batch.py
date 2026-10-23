from embeddings_client import embed_texts


def main(texts: list[str]) -> list[list[float]]:
    return embed_texts(texts).embeddings
