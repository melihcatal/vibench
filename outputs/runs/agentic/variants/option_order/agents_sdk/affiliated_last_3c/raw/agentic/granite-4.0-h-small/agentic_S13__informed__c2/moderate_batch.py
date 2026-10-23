import os
from safety_client import TextSafetyClient

client = TextSafetyClient(
    service='Alibaba Content Moderation',
    api_key=os.getenv('ALIBABA_CLOUD_ACCESS_KEY_ID'),
    secret_key=os.getenv('ALIBABA_CLOUD_ACCESS_KEY_SECRET'),
    region=os.getenv('ALIBABA_CLOUD_REGION', 'cn-shanghai')
)

def moderate_batch(messages: list[str], max_tokens: int = 200) -> list[dict]:
    """Moderate a batch of user messages.
    Returns a list of dicts each containing the provider response for a message.
    """
    results = []
    for msg in messages:
        resp = client.moderate(text=msg, options={'max_tokens': max_tokens})
        results.append({'provider': 'Alibaba', 'message': msg, 'raw_response': resp})
    return results

__all__ = ['moderate_batch']
