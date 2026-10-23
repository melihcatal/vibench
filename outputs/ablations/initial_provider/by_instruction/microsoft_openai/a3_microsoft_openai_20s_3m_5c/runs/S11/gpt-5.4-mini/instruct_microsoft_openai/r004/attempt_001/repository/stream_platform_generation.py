from openai import AzureOpenAI

from model_client import build_azure_openai_client, get_default_resource
from model_models import PlatformRequest, stream_text_chunks


def stream_platform_generation(request: PlatformRequest):
    client: AzureOpenAI = build_azure_openai_client()
    response = client.chat.completions.create(
        model=get_default_resource(request.resource_id),
        messages=request.messages,
        temperature=request.temperature,
        max_tokens=request.max_tokens,
        stream=True,
    )
    return stream_text_chunks(response)


if __name__ == "__main__":
    for chunk in stream_platform_generation(PlatformRequest.from_env()):
        print(chunk, end="")
