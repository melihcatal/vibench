import os
from model_client import get_platform_client, get_deployment
from model_models import ChatMessage, ChatRequest

def invoke_platform_model(prompt: str, model_family: str = "gpt-4o") -> str:
    client = get_platform_client()
    deployment = get_deployment(model_family)
    messages: list[ChatMessage] = [{"role": "user", "content": prompt}]
    request: ChatRequest = {
        "model": deployment,
        "messages": messages,
        "max_tokens": 500
    }
    response = client.chat.completions.create(**request)
    return response.choices[0].message.content
