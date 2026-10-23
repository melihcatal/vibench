from typing import Dict, Any, Tuple
from model_client import ModelClient
from model_models import ModelResponse, PlatformMetadata
from azure.ai.inference.models import ChatCompletionsResponse


def collect_platform_metadata(
    request: Dict[str, Any],
) -> Tuple[ModelResponse, PlatformMetadata]:
    """Returns Azure AI Inference model output with platform metadata."""
    client = ModelClient().get_client()

    messages = ModelClient().prepare_messages(
        system_prompt=request["system_prompt"], user_prompt=request["user_prompt"]
    )

    response: ChatCompletionsResponse = client.complete(
        messages=messages,
        model="gpt-4o",
        temperature=request.get("temperature", 0.7),
        max_tokens=request.get("max_tokens", 1000),
    )

    model_response = ModelResponse(
        id=response.id,
        content=response.choices[0].message.content,
        finish_reason=response.choices[0].finish_reason,
        usage={
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens,
        },
        model=response.model,
    )

    metadata = PlatformMetadata(
        model=response.model,
        deployment_id="gpt-4o-deployment",
        usage=model_response.usage,
        system_fingerprint=response.system_fingerprint,
        invocation_id=response.id,
    )

    return model_response, metadata
