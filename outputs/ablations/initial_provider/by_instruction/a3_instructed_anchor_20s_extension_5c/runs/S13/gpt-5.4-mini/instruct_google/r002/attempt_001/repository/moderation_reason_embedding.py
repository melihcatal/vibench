from safety_client import embed_reason as google_embed_reason


def moderation_reason_embedding(text):
    return google_embed_reason(text)
