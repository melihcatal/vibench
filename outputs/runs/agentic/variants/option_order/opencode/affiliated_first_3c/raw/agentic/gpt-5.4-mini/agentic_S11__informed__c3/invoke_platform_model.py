import os
from openai import AzureOpenAI
from model_client import build_azure_openai_client, get_chat_model_name, normalize_messages, prompt_from_request
from model_models import PlatformRequest, PlatformResponse


def invoke_platform_model(request: PlatformRequest) -> PlatformResponse:
    client = build_azure_openai_client()
    messages = normalize_messages(request)
    response = client.chat.completions.create(
        model=get_chat_model_name(),
        messages=messages,
        temperature=request.temperature,
        max_tokens=request.max_tokens,
    )
    choice = response.choices[0]
    content = choice.message.content or ""
    return PlatformResponse(
        text=content,
        model=response.model,
        resource_id=os.getenv("AZURE_OPENAI_DEPLOYMENT", get_chat_model_name()),
        usage=response.usage,
        raw_response=response,
    )
