import os
from model_client import ManagedModelClient


def invoke_model(deployment_name: str, prompt: str):
    # Load client configured for a specific provider (e.g., Hugging Face Inference API)
    client = ManagedModelClient()
    # Resolve the specific model/deployment using the helper (select_platform_resource.py would be called before)
    model_id = select_platform_resource(resolve_model=deployment_name)
    # Invoke the provider-managed model
    response = client.invoke(model_id=model_id, prompt=prompt)
    return response
