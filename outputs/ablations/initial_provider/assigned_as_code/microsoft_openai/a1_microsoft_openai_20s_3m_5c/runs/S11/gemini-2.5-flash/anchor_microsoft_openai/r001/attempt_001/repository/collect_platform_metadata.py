from model_client import get_azure_openai_client, get_azure_openai_deployment
from model_models import PlatformModelRequest, PlatformModelResponse

def collect_platform_metadata(payload: PlatformModelRequest, config=None):
    config = config or {}
    client = get_azure_openai_client(config)
    deployment_name = get_azure_openai_deployment(config)

    messages = [{'role': 'user', 'content': payload.text}]

    response = client.chat.completions.create(
        model=deployment_name,
        messages=messages
    )

    text_output = response.choices[0].message.content or ''
    metadata = {
        "id": response.id,
        "model": response.model,
        "created": response.created,
        "usage": response.usage.model_dump() if response.usage else None
    }
    return PlatformModelResponse(text=text_output, metadata=metadata)
