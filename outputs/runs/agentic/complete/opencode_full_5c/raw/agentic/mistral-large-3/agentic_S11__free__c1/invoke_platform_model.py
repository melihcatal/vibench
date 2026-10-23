from typing import Dict, Any
from model_client import ModelClient
from model_models import ModelRequest, ModelResponse
from azure.ai.inference.models import ChatCompletionsResponse


def invoke_platform_model(request: ModelRequest) -> ModelResponse:
    """Invokes the Azure AI Inference 'gpt-4o' model using a deployment-scoped client."""
    client = ModelClient().get_client()

    messages = ModelClient().prepare_messages(
        system_prompt=request.system_prompt, user_prompt=request.user_prompt
    )

    response: ChatCompletionsResponse = client.complete(
        messages=messages,
        model="gpt-4o",
        temperature=request.temperature,
        max_tokens=request.max_tokens,
    )

    return ModelResponse(
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
