import os
from model_client import ManagedModelClient
from model_models import RequestPayload, ResponseWrapper
import requests

def embed_text(text: str, model_id: str = 'text-embedding-ada-002') -> ResponseWrapper:
    """Embed a string using Azure OpenAI embeddings endpoint.
    Returns a response wrapper with vector and metadata.
    """
    endpoint = f"{os.getenv('AZURE_OPENAI_ENDPOINT')}/openai/embeddings/deployments/{model_id}/json"
    headers = {
        "api-key": os.getenv('AZURE_OPENAI_API_KEY'),
        "Content-Type": "application/json"
    }
    payload = {
        "input": text
    }
    resp = requests.post(endpoint, json=payload, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    # Example expected shape: data['data'][0]['embedding']
    vec = data['data'][0]['embedding']
    usage = data.get('usage')
    return ResponseWrapper(output=vec, metadata={'provider': 'azure_openai', 'model': model_id, 'usage': usage})

client = ManagedModelClient(provider='huggingface', token=os.getenv('HF_TOKEN'))
def embed_and_collect(model_id: str, payload: RequestPayload) -> ResponseWrapper:
    raw = client.invoke(model_id=model_id, payload=payload)
    # If model supports embeddings natively, use its output; otherwise fallback to Azure OpenAI
    if 'error' not in raw:
        vec = raw.get('embedding')
    else:
        vec = embed_text(payload['inputs'], model_id='text-embedding-ada-002').output
    return ResponseWrapper(output=vec, metadata={'provider': 'huggingface', 'model_id': model_id})

# Minimal test (uncomment)
# if __name__ == '__main__':
#     payload = RequestPayload(inputs="The quick brown fox jumps over the lazy dog.")
#     result = embed_and_collect('facebook/opt-1.3b', payload)
#     print(result)
