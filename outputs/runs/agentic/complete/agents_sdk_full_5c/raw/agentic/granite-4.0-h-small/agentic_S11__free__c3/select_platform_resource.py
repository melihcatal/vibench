import os
from model_models import ModelResource

def select_platform_resource(deployment_name=None, model_id=None, infer_profile=None):
    """Resolve a concrete provider resource identifier for invocation.
    Demonstrates selection logic for OpenAI's GPT-4o model via environment
    variables or provided arguments. Returns a ModelResource instance that
    encapsulates the provider-specific handle.
    """
    # Choose source priority: explicit argument > inference profile > env var
    if model_id is not None:
        return ModelResource(provider="openai", model=model_id)
    if deployment_name is not None:
        return ModelResource(provider="openai", deployment=deployment_name)

    # Fallback to a well-known deployment via env var
    dep_env = os.getenv("DEFAULT_DEPLOYMENT_ID")
    if dep_env:
        return ModelResource(provider="openai", deployment=dep_env)
    raise ValueError("No resource identifier supplied")

# Example usage for local testing
if __name__ == "__main__":
    from model_client import ManagedModelClient
    client = ManagedModelClient()
    resource = select_platform_resource()
    print("Selected resource:", resource)
    print("Provider name:", client.provider_name())
