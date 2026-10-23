from model_client import get_azure_openai_client
from model_models import ModelRequest
from select_platform_resource import select_platform_resource


def invoke_platform_model(request: ModelRequest, model_family: str = "gpt-4o"):
    client = get_azure_openai_client()
    deployment = select_platform_resource(model_family)
    openai_request = {
        "model": deployment,
        "messages": request["messages"],
        "max_tokens": request.get("max_tokens", 1000),
        "temperature": request.get("temperature", 0.7),
    }
    response = client.chat.completions.create(**openai_request)
    content = response.choices[0].message.content
    usage = {
        "prompt_tokens": response.usage.prompt_tokens,
        "completion_tokens": response.usage.completion_tokens,
        "total_tokens": response.usage.total_tokens,
    }
    return {
        "content": content,
        "usage": usage,
        "model": deployment,
    }
