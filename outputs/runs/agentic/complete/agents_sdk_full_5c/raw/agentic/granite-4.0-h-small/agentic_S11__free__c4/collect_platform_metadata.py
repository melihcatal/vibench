# collect_platform_metadata.py
# [SAME-SCENARIO] Return model output together with provider platform metadata

from model_client import ManagedModelClient
from model_models import ModelInvocationRequest, ModelInvocationResponse


def collect_platform_metadata(
    deployment_name: str,
    prompt: str,
) -> dict:
    """Invokes a model and augments the raw provider response with usage and resource metadata.

    Returns a single dict containing:
        - 'output': the LLM model response
        - 'metadata': provider-specific usage, request ID, deployment ID, model handle
    """
    client = ManagedModelClient()  # Azure OpenAI client
    request = ModelInvocationRequest(
        deployment=deployment_name,
        prompt=prompt,
    )
    raw_response = client.invoke_model(request)  # provider API call
    # Merge usage info (example fields for Azure OpenAI)
    usage = raw_response.get("usage", {})
    # Construct the enriched payload
    enriched = {
        "output": raw_response,
        "metadata": {
            "deployment_id": raw_response.get("deployment_id"),
            "model_handle": raw_response.get("model"),
            "request_id": raw_response.get("request_id"),
            "usage": usage,
        },
    }
    return enriched

if __name__ == "__main__":
    # Example usage
    result = collect_platform_metadata(deployment_name="gpt-4o", prompt="Hello")
    print(result)
