import os
from safety_client import SafetyClient

client = SafetyClient()


def embed_moderation_reason(reason):
    embedding = client.embed_moderation_reason(reason)
    return embedding
