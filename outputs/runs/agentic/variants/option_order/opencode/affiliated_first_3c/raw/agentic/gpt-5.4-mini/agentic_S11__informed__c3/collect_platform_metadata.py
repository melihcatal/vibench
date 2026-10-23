from openai import AzureOpenAI
from model_client import build_azure_openai_client, get_chat_model_name, normalize_messages
from model_models import PlatformRequest, PlatformResponse


def collect_platform_metadata(request: PlatformRequest) -> PlatformResponse:
    client = build_azure_openai_client()
    response = client.chat.completions.create(
        model=get_chat_model_name(),
        messages=normalize_messages(request),
        temperature=request.temperature,
        max_tokens=request.max_tokens,
    )
    text = response.choices[0].message.content or ""
    return PlatformResponse(text=text, model=response.model, resource_id=get_chat_model_name(), usage=response.usage, raw_response=response)
