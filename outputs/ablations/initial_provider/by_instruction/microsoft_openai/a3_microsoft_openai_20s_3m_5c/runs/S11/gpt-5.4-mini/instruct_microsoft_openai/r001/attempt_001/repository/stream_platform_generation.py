from model_client import get_azure_openai_client
from model_models import ModelRequest
from select_platform_resource import select_platform_resource


def stream_platform_generation(request: ModelRequest):
    client = get_azure_openai_client()
    resource = select_platform_resource()
    deployment = request.model or resource["deployment"]
    return client.chat.completions.create(
        model=deployment,
        messages=[{"role": "user", "content": request.prompt}],
        temperature=request.temperature,
        max_tokens=request.max_tokens,
        stream=True,
    )
