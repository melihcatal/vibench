from model_client import get_platform_client
from model_models import ChatCompletionRequest

def collect_platform_metadata(request: ChatCompletionRequest):
    client = get_platform_client()
    response = client.chat.completions.create(**request)
    choice = response.choices[0]
    metadata = {
        "content": choice.message.content,
        "model": getattr(response, "model", None),
        "id": getattr(response, "id", None),
        "usage": {
            "prompt_tokens": getattr(response.usage, "prompt_tokens", 0),
            "completion_tokens": getattr(response.usage, "completion_tokens", 0),
            "total_tokens": getattr(response.usage, "total_tokens", 0),
        }
    }
    return metadata
