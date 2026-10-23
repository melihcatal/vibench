import os
from model_client import ManagedModelClient
from model_models import ModelInvocationRequest, ModelInvocationResponse

def platform_output_safety(raw_response: ModelInvocationResponse) -> bool:
    """Check generated text for unsafe or disallowed content using a provider guardrail."""
    # Azure OpenAI Content Safety endpoint (example)
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    if not endpoint or not key:
        raise RuntimeError("Content Safety credentials not configured")

    import requests
    url = f"{endpoint}/v1/moderations"
    headers = {
        "api-key": key,
        "Content-Type": "application/json",
    }
    payload = {
        "input": raw_response.output,
        "model": "default",
    }
    resp = requests.post(url, json=payload, headers=headers)
    resp.raise_for_status()
    moderation = resp.json()
    # The moderation response contains an array of results.
    safe = moderation["results"][0]["flagged"] == False
    return safe


if __name__ == "__main__":
    # Example usage with Azure OpenAI deployment
    AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
    DEPLOYMENT_ID = "gpt-4o-mini"
    prompt = "Write a short story about a bank robbery."
    resp = ManagedModelClient().invoke(ModelInvocationRequest(DEPLOYMENT_ID, prompt))
    if platform_output_safety(resp):
        print("Content is safe")
    else:
        print("Content flagged as unsafe")