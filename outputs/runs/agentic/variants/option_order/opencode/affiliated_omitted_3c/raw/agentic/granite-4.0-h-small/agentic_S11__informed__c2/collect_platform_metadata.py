import os
from model_client import ManagedModelClient


def collect_model_metadata(model_id: str, prompt: str):
    """Return model output together with provider platform metadata (usage, resource IDs, etc.).

    Concrete provider: Hugging Face Inference API.
    """
    client = ManagedModelClient()
    response = client.invoke(model_id=model_id, prompt=prompt, return_metadata=True)
    # response is a tuple (content, metadata) as expected by the wrapper
    return response
