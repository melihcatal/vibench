from openai import AzureOpenAI
from model_client import build_azure_openai_client, get_chat_model_name, normalize_messages
from model_models import PlatformRequest


def stream_platform_generation(request: PlatformRequest):
    client = build_azure_openai_client()
    stream = client.chat.completions.create(
        model=get_chat_model_name(),
        messages=normalize_messages(request),
        temperature=request.temperature,
        max_tokens=request.max_tokens,
        stream=True,
    )
    for chunk in stream:
        yield chunk
