from openai import AzureOpenAI

from model_client import build_azure_openai_client, get_default_resource
from model_models import PlatformRequest, collect_response_payload


def collect_platform_metadata(request: PlatformRequest):
    client: AzureOpenAI = build_azure_openai_client()
    response = client.chat.completions.create(
        model=get_default_resource(request.resource_id),
        messages=request.messages,
        temperature=request.temperature,
        max_tokens=request.max_tokens,
    )
    return collect_response_payload(response)


if __name__ == "__main__":
    print(collect_platform_metadata(PlatformRequest.from_env()))
