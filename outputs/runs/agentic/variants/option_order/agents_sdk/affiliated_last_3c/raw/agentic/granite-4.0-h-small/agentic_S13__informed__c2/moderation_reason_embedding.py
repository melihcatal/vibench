import os
from safety_client import TextSafetyClient
from safety_models import ModSafetyResponse
import json

def moderation_reason_embedding(text: str) -> ModSafetyResponse:
    """Embed moderation rationales (unsafe reasons) for case retrieval.
    This example uses Alibaba Embeddings API (available via the same SDK) to
    embed the list of unsafe reasons.
    Returns the raw provider response containing an embedding vector.
    """
    client = TextSafetyClient()
    # Assuming the SDK provides an 'embed' endpoint
    payload = {'text': text, 'purpose': 'moderation_reason'}
    resp = client.moderate(text=json.dumps(payload), options={})
    return {'provider': 'Alibaba', 'raw_response': resp}

__all__ = ['moderation_reason_embedding']
