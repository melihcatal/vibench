import os
from model_models import ModelRequest
from model_client import ManagedModelClient

def select_deployment(request: ModelRequest) -> str:
    """Return the provider-specific deployment name for the model referenced in the request."""
    provider = request.config.get("provider", "anthropic")
    if provider == "anthropic":
        return request.config.get("deployment", "claude-3-5-sonnet-v1.0")
    elif provider == "openai":
        return request.config.get("deployment", "gpt-4o-mini")
    raise ValueError(f"Unsupported provider: {provider}")

if __name__ == "__main__":
    # Demo usage
    demo_req = ModelRequest(payload={"user": "Hello"}, config={"provider": "anthropic"})
    print("Selected deployment:", select_deployment(demo_req))
