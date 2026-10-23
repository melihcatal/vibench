from embedder_client import embedder


def moderation_reason_embedding(text):
    embedding = embedder.embed_text(text)
    return embedding
