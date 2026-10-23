import os
import json
from model_client import ManagedModelClient

def invoke_platform_model(deployment_id, prompt, **kwargs):
    """Invoke a managed model via the provider client and return raw response.
    Uses OpenAI's GPT-4o (or compatible) as the concrete provider.
    """
    client = ManagedModelClient()  # loads provider-specific env vars
    # Identify provider in code
    provider_name = client.provider_name()  # e.g., "openai"
    print(f"Invoking {provider_name} deployment {deployment_id}...")
    response = client.invoke_model(deployment_id, prompt, **kwargs)
    return response

if __name__ == "__main__":
    # Example usage (remove or adjust for production)
    deployment = os.getenv("DEPLOYMENT_ID")
    txt = "Hello, how are you?"
    raw = invoke_platform_model(deployment, txt)
    print(json.dumps(raw, indent=2))
