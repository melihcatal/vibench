import os
from openai import AzureOpenAI

from model_client import build_azure_openai_client, get_chat_model_name, get_default_resource
from model_models import PlatformRequest, normalize_text_response


def invoke_platform_model(request: PlatformRequest) -> str:
    client = build_azure_openai_client()
    resource = get_default_resource(request.resource_id)
    response = client.chat.completions.create(
        model=resource,
        messages=request.messages,
        temperature=request.temperature,
        max_tokens=request.max_tokens,
    )
    return normalize_text_response(response)


def main() -> None:
    request = PlatformRequest.from_env()
    print(invoke_platform_model(request))


if __name__ == "__main__":
    main()
