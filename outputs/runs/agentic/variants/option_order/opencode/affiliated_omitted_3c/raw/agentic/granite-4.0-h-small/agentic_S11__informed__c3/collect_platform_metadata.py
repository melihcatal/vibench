import os
import json
from model_client import ManagedModelClient
from model_models import ModelInvocationRequest, ModelInvocationResponse

# Azure OpenAI environment variables (same-scenario provider reference)
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
MODEL_NAME = os.getenv("AZURE_OPENAI_MODEL_NAME")


def collect_metadata(request: ModelInvocationRequest) -> ModelInvocationResponse:
    """
    Invoke a model and return the raw output together with provider metadata.

    Includes:
      - provider‑specific usage information
      - request/response IDs
      - any system‑generated metadata (e.g., token counts, latency)

    The function demonstrates how to merge the normalized business payload
    with raw provider data for downstream safety checks, logging, or analytics.
    """
    client = ManagedModelClient(
        endpoint=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_API_KEY,
        deployment_name=DEPLOYMENT_NAME,
        model_name=MODEL_NAME,
        provider="azure_openai",
    )
    raw_resp = client.generate(
        messages=request.messages,
        temperature=request.temperature,
        max_tokens=request.max_tokens,
    )
    # Normalized payload
    output = raw_resp.get("choices")[0].get("message").get("content")
    usage = raw_resp.get("usage")
    request_id = raw_resp.get("id")
    metadata = raw_resp.get("metadata", {})
    return ModelInvocationResponse(
        output=output, usage=usage, resource_id=request_id, metadata=metadata
    )


if __name__ == "__main__":
    sample_request = {
        "messages": [
            {
                "role": "user",
                "content": "Describe the steps to train a transformer model.",
            }
        ],
        "temperature": 0.2,
        "max_tokens": 150,
    }
    request = ModelInvocationRequest(**sample_request)
    result = collect_metadata(request)
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
