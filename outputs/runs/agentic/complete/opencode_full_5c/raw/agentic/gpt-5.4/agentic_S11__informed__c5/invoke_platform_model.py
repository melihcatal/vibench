from __future__ import annotations

from model_client import get_azure_openai_client, get_chat_deployment
from model_models import PlatformRequest, extract_text


def invoke_platform_model(request: PlatformRequest) -> str:
    client = get_azure_openai_client()
    response = client.chat.completions.create(
        model=get_chat_deployment(),
        messages=request.to_messages(),
        temperature=request.temperature,
        max_tokens=request.max_tokens,
    )
    return extract_text(response.choices[0].message)
