from embeddings_client import embed_texts


def generate_embedding(text: str):
    return embed_texts(text).embeddings[0]
