import os
import json
from model_client import ManagedModelClient
from model_models import ModelInvocationRequest, ModelInvocationResponse

# Example using Azure OpenAI Service (Azure AI Foundry)
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
MODEL_NAME = os.getenv("AZURE_OPENAI_MODEL_NAME")


def invoke(model_request: ModelInvocationRequest) -> ModelInvocationResponse:
    """Invoke a provider-managed generative model via the Azure OpenAI SDK.

    Args:
        model_request: Encapsulated request payload.

    Returns:
        Response containing model output, usage, and metadata.
    """
    client = ManagedModelClient(
        endpoint=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_API_KEY,
        deployment_name=DEPLOYMENT_NAME,
        model_name=MODEL_NAME,
        provider="azure_openai",
    )
    raw_response = client.generate(
        messages=model_request.messages,
        temperature=model_request.temperature,
        max_tokens=model_request.max_tokens,
    )
    # Normalize raw SDK response into our standard response model
    normalized = client.normalize_response(raw_response)
    return ModelInvocationResponse(
        output=normalized.get("choices")[0].get("message").get("content"),
        usage=normalized.get("usage"),
        resource_id=normalized.get("id"),
        metadata=normalized.get("metadata"),
    )


if __name__ == "__main__":
    # Simple demo payload
    payload = {
        "messages": [
            {
                "role": "user",
                "content": "Hello, explain quantum computing in two sentences.",
            }
        ],
        "temperature": 0.7,
        "max_tokens": 100,
    }
    request = ModelInvocationRequest(**payload)
    result = invoke(request)
    print(
        json.dumps(
            {
                "output": result.output,
                "usage": result.usage,
                "resource_id": result.resource_id,
                "metadata": result.metadata,
            },
            indent=2,
        )
    )
