import json
from model_client import ManagedModelClient
from model_models import NormalizedResponse

async def collect_platform_metadata(deployment_id, prompt, *, extra_params=None):
    """Invoke a managed model and return both the model output and provider-specific metadata.
    The function returns a dict containing:
        - 'output': normalized response data
        - 'metadata': provider-specific fields such as usage, model, request_id, etc.
    Uses OpenAI's API as the concrete provider.
    """
    client = ManagedModelClient()
    provider_name = client.provider_name()  # e.g., "openai"
    print(f"Collecting metadata from {provider_name} deployment {deployment_id}...")

    # Prepare request parameters, merging any extra_params
    params = {
        "model": deployment_id,
        "prompt": prompt,
    }
    if extra_params:
        params.update(extra_params)

    # Use client to fetch raw response (with streaming disabled for full response)
    raw = client.invoke_model(deployment_id, prompt, stream=False, **(extra_params or {}))
    # Normalize response (example normalization for OpenAI JSON format)
    normalized = NormalizedResponse.from_openai(raw)

    # Extract metadata that OpenAI adds to its response objects
    metadata = {
        "usage": raw.get("usage", {}),
        "model": raw.get("model"),
        "request_id": raw.get("id"),
        "timestamp": raw.get("created"),
        "provider": provider_name,
    }

    # Assemble combined result
    result = {
        "output": normalized.data,
        "metadata": metadata,
    }
    return result

# Local example usage
if __name__ == "__main__":
    import os
    deployment = os.getenv("DEPLOYMENT_ID")
    text = "Give me a short summary of the capital of France."
    result = collect_platform_metadata(deployment, text)
    print(json.dumps(result, indent=2))
