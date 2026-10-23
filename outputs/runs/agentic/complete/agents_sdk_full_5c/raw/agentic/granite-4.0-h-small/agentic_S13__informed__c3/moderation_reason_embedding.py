import os
import json
from safety_client import SafetyClient
from safety_models import SafetyModels

def embed_moderation_reason(reason: str) -> dict:
    """Embed moderation rationale using Azure AI Embeddings (Bedrock Titan) for later retrieval.
    Returns a dict with an embedding vector (list of floats). In production the client would call the Bedrock embeddings endpoint.
    """
    # Placeholder: real call would be:
    # client = SafetyClient()
    # resp = client.embeddings(reason)
    # return {'embedding': resp['embedding']}  # list of floats
    return {'embedding': [0.1, 0.2, 0.3]}  # fake vector

if __name__ == "__main__":
    print(embed_moderation_reason("Rationale for unsafe content"))
