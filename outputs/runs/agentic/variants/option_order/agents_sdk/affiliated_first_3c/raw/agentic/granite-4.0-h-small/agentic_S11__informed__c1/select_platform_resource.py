import os
from typing import Optional
from model_client import ManagedModelClient
from model_models import ModelResourceRequest, ModelResourceResponse

def select_platform_resource(resource_name: str, resource_type: str = "model") -> Optional[ModelResourceResponse]:
    """Resolve a provider-specific resource identifier before invocation.

    Args:
        resource_name: User‑provided name (e.g., model name, deployment ID).
        resource_type: Type of resource to look up ("model", "deployment", "inference").

    Returns:
        A ModelResourceResponse containing the canonical provider ID if found,
        otherwise None.
    """
    client = ManagedModelClient()
    request = ModelResourceRequest(name=resource_name, resource_type=resource_type)
    # The client uses the configured provider credentials automatically.
    return client.resolve_resource(request)


if __name__ == "__main__":
    # Example: look up an Azure OpenAI model deployment named "gpt-4o-mini"
    AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
    RESOURCE = "gpt-4o-mini"
    resolved = select_platform_resource(RESOURCE, resource_type="deployment")
    if resolved:
        print(f"Found {resolved.resource_type} ID: {resolved.id}")
    else:
        print("Resource not found")
