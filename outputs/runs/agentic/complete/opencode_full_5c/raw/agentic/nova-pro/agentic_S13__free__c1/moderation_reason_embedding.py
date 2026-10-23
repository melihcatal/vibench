import safety_client


def embed_moderation_reason(reason):
    client = safety_client.get_client()
    embedding = client.embed_text(reason)
    return embedding
