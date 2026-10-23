import os
from model_client import ManagedModelClient
from model_models import ModelInvocationRequest, ModelInvocationResponse

def collect_platform_metadata(deployment_id: str, prompt: str) -> ModelInvocationResponse:
    """Invoke a model and return the full provider‑specific response object,
    including usage, resource IDs, and any ancillary metadata.

    Returns:
        ModelInvocationResponse containing both output text and metadata.
    """
    client = ManagedModelClient()
    request = ModelInvocationRequest(deployment_id=deployment_id, prompt=prompt)
    return client.invoke(request)


if __name__ == "__main__":
    # Example with Azure OpenAI
    AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
    DEPLOYMENT_ID = "gpt-4o-mini"
    prompt = "What is the square root of 121?"
    result = collect_platform_metadata(DEPLOYMENT_ID, prompt)
    # The response object contains structured fields from the provider.
    print("Output:", result.output)
    print("Usage info:", result.usage)
    print("Resource ID:", result.resource_id)