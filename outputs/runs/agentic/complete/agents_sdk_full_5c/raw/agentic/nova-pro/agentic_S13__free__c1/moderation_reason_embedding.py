from safety_client import get_safety_client

def moderation_reason_embedding(text):
    client = get_safety_client()
    embedding = client.embed_text(text)
    return embedding