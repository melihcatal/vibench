import os
from model_client import get_platform_client, get_deployment
from model_models import ChatMessage, Usage

def collect_platform_metadata(prompt: str, model_family: str = "gpt-4o") -> dict:
    client = get_platform_client()
    deployment = get_deployment(model_family)
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=deployment,
        messages=messages,
        max_tokens=500
    )
    choice = response.choices[0]
    usage: Usage = {
        "prompt_tokens": response.usage.prompt_tokens,
        "completion_tokens": response.usage.completion_tokens,
        "total_tokens": response.usage.total_tokens
    } if response.usage else {}
    return {
        "output": choice.message.content,
        "model": deployment,
        "usage": usage,
        "response_id": response.id,
        "finish_reason": choice.finish_reason
    }
