import os
import json
from model_client import ManagedModelClient
from model_models import (
    ModelInvocationRequest,
    ModelInvocationResponse,
    StreamedOutputChunk,
)

# Azure OpenAI safety detection client (same‑scenario provider)
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
CONTENT_SAFETY_RESOURCE_ID = os.getenv("AZURE_OPENAI_CONTENT_SAFETY_RESOURCE_ID")


async def check_safety(
    model_response: ModelInvocationResponse,
) -> ModelInvocationResponse:
    """
    Post‑process a model response to detect unsafe content using Azure Content Safety API.
    The function returns the original response augmented with a `safety` field containing the API verdict.

    Note: This implementation uses the Azure Content Safety SDK, but the pattern can be swapped for
    any provider (e.g., Perspective API, Alibaba Content Moderation) by changing the selector in
    `select_platform_resource`.
    """
    # Placeholder: in production install azure-ai-contentsafety and import its classes.
    # from azure.ai.contentsafety import ContentSafetyClient
    # client = ContentSafetyClient(endpoint=AZURE_OPENAI_ENDPOINT, credential=AzureKeyCredential(AZURE_OPENAI_API_KEY))
    # safety_result = await client.analyze_content(model_response.output)
    # For demo purposes we simulate a safety check (always "SAFE").
    safety_result = {"outcome": "SAFE", "details": []}

    # Merge safety outcome into the response metadata
    return ModelInvocationResponse(
        output=model_response.output,
        usage=model_response.usage,
        resource_id=model_response.resource_id,
        metadata={**(model_response.metadata or {}), "safety_check": safety_result},
    )


if __name__ == "__main__":

    async def demo():
        payload = {
            "messages": [
                {"role": "user", "content": "Write a short story about a bank robbery."}
            ],
            "temperature": 0.5,
            "max_tokens": 120,
        }
        request = ModelInvocationRequest(**payload)
        client = ManagedModelClient(
            endpoint=AZURE_OPENAI_ENDPOINT,
            api_key=AZURE_OPENAI_API_KEY,
            deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            model_name=os.getenv("AZURE_OPENAI_MODEL_NAME"),
            provider="azure_openai",
        )
        raw_resp = await client.generate(
            payload["messages"], payload["temperature"], payload["max_tokens"]
        )
        resp = ModelInvocationResponse(
            output=raw_resp.get("choices")[0].get("message").get("content"),
            usage=raw_resp.get("usage"),
            resource_id=raw_resp.get("id"),
            metadata=raw_resp.get("metadata", {}),
        )
        safe_resp = await check_safety(resp)
        print(
            json.dumps(
                {
                    "safe_output": safe_resp.output,
                    "safety": safe_resp.metadata["safety_check"],
                },
                indent=2,
            )
        )

    asyncio.run(demo())
