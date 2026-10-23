import os
from model_client import ManagedModelClient
from model_models import ModelInvocationRequest, ModelInvocationMetadata

def platform_output_safety(model_output: str) -> bool:
    """
    Check generated content for disallowed material using a provider moderation service.
    This example uses Azure Content Safety (could be swapped for Bedrock Guardrails, Perspective, etc.).
    Returns True if the content is safe, False otherwise.
    """
    # Instantiate moderation client (requires environment vars)
    client = ManagedModelClient()  # Reuse generic client placeholder
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    if not (endpoint and key):
        raise RuntimeError("Azure Content Safety credentials not configured")
    # Simple request using requests library (requests is in the environment)
    import requests
    resp = requests.post(
        f"{endpoint}/contentsafety/v1.0/moderations",
        json={"input": model_output},
        headers={"api-key": key},
    )
    result = resp.json()
    # Assume result format: {"results": [{"flagged": bool, "categories": {...}}]}
    flagged = result.get("results", [{}])[0].get("flagged", False)
    return not flagged

# Example safety check (uncomment for local demo)
# if __name__ == "__main__":
#     output = "I will tell you how to hack this system."
#     print("Safe?", platform_output_safety(output))
