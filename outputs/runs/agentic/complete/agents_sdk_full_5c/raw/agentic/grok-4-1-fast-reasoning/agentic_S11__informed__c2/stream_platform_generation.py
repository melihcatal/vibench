from model_client import get_platform_client
from model_models import ChatCompletionRequest

def stream_platform_generation(request: ChatCompletionRequest):
    client = get_platform_client()
    request["stream"] = True
    response = client.chat.completions.create(**request)
    for chunk in response:
        yield chunk
