from embeddings_client import embed_texts


def embed_batch(texts):
    return embed_texts(texts).embeddings
