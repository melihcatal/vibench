from safety_client import embed_text


def moderation_reason_embedding(reason):
    return embed_text(reason)
