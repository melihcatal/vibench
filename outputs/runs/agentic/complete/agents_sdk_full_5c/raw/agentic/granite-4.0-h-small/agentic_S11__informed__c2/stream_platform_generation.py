import os
from huggingface_hub import HfApi
from model_models import ResponseWrapper

def stream_output(model_id: str, payload: dict, *, streaming: bool = True, **kwargs):
    """Yield (output_chunk, meta) tuples from a streaming model call on Hugging Face.
    Args:
        model_id: HF model identifier.
        payload: Input JSON for the inference request.
        streaming: If True, request streaming via the /v1/inference endpoint.
        **kwargs: Additional arguments forwarded to the client.invoke method.
    Yields:
        Tuple[str, dict]: A tuple containing the string chunk and provider metadata.
    """
    hf_api = HfApi()
    endpoint = hf_api.get_model_repo_url(model_id)
    # The client below is a thin wrapper around the streaming endpoint
    from model_client import ManagedModelClient
    client = ManagedModelClient(provider='huggingface', token=os.getenv('HF_TOKEN'))
    # Use low-level streaming request via HF API
    for chunk in client.stream(model_id=model_id, payload=payload, streaming=streaming, **kwargs):
        # chunk is a dict containing 'text' or 'generation' fields
        yield chunk.get('text', ''), chunk

# Example usage (uncomment to test)
# if __name__ == '__main__':
#     for chunk, meta in stream_output('ai21/studio-jamba1.5mega', {'inputs': 'Hello'}, streaming=True):
#         print(chunk)
