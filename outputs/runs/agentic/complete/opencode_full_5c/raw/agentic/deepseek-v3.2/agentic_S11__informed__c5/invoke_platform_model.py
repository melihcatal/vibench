import os
from openai import AzureOpenAI
from model_client import get_azure_client
from model_models import ChatRequest, ChatResponse


def invoke_platform_model(request: ChatRequest) -> ChatResponse:
    """
    Invoke a provider-managed model through Azure OpenAI deployment.
    """
    client = get_azure_client()

    try:
        response = client.chat.completions.create(
            model=request.model,
            messages=request.messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            stream=False,
        )

        return ChatResponse(
            content=response.choices[0].message.content,
            model=response.model,
            usage=response.usage,
            finish_reason=response.choices[0].finish_reason,
            raw_response=response,
        )
    except Exception as e:
        raise RuntimeError(f"Failed to invoke Azure OpenAI model: {e}")
