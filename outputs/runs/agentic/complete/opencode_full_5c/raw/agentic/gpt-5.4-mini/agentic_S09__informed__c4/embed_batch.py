from embeddings_client import embed_texts


def generate_embeddings(texts):
    return embed_texts(texts).embeddings
