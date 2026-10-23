from model_client import get_azure_openai_client, get_azure_openai_deployment
from model_models import PlatformModelRequest

def stream_platform_generation(payload: PlatformModelRequest, config=None):
    config = config or {}
    client = get_azure_openai_client(config)
    deployment_name = get_azure_openai_deployment(config)

    messages = [{'role': 'user', 'content': payload.text}]

    stream_response = client.chat.completions.create(
        model=deployment_name,
        messages=messages,
        stream=True
    )

    for chunk in stream_response:
        yield chunk
