from openai import AzureOpenAI
from model_models import ModelRequest, ModelResponse, ChatMessage
from model_client import get_azure_openai_config


def invoke_platform_model(request: ModelRequest) -> ModelResponse:
    config = get_azure_openai_config()
    client = AzureOpenAI(**config)
    response = client.chat.completions.create(
        model=request.deployment,
        messages=[msg.model_dump() for msg in request.messages],
        temperature=request.temperature,
        max_tokens=request.max_tokens,
    )
    return ModelResponse(
        id=response.id,
        content=response.choices[0].message.content,
        usage=response.usage.model_dump() if response.usage else None,
    )
