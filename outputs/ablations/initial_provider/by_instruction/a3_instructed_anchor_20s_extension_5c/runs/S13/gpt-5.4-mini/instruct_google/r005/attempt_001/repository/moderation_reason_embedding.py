from safety_client import embeddings


def moderation_reason_embedding(text: str):
    return embeddings([text])[0]
