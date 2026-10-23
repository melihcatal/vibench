from model_client import get_platform_client
from model_models import ChatCompletionRequest

def invoke_platform_model(request: ChatCompletionRequest):
    client = get_platform_client()
    response = client.chat.completions.create(**request)
    return response.choices[0].message.content
