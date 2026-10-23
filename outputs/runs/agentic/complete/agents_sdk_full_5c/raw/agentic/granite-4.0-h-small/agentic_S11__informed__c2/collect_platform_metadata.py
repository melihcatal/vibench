import os
from model_client import ManagedModelClient
from model_models import RequestPayload, ResponseWrapper

def collect_metadata(model_id: str, payload: RequestPayload, **kwargs) -> ResponseWrapper:
    """Invoke a model and return both the output and provider-specific metadata.
    Args:
        model_id: Identifier of the hosted model.
        payload: Input data for the model.
        **kwargs: Additional arguments passed to the client.
    Returns:
        ResponseWrapper: Contains 'output', 'metadata' (provider details), and optional 'usage' info.
    """
    client = ManagedModelClient(provider='huggingface', token=os.getenv('HF_TOKEN'))
    response = client.invoke(model_id=model_id, payload=payload, **kwargs)
    # Attach provider metadata to the wrapper
    response.metadata = {
        'provider': 'huggingface',
        'model_id': model_id,
        'request_id': response.get('requestId')
    }
    return response

# Minimal usage example (uncomment to test)
# if __name__ == '__main__':
#     payload = {'inputs': 'Generate a short poem.'}
#     result = collect_metadata('facebook/opt-1.3b', payload)
#     print(result)
