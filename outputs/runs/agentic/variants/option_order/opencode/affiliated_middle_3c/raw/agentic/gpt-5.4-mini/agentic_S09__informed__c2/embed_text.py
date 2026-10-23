from embeddings_client import embed_texts


def main(text: str) -> list[float]:
    return embed_texts([text]).embeddings[0]
