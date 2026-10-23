from model_client import get_client
from typing import List, Dict, Any


def collect_platform_metadata(
    messages: List[Dict[str, str]], deployment_id: str
) -> Dict[str, Any]:
    client = get_client()
    response = client.chat.completions.create(
        model=deployment_id,
        messages=messages,
        max_tokens=1000,
    )
    usage = {
        "prompt_tokens": response.usage.prompt_tokens,
        "completion_tokens": response.usage.completion_tokens,
        "total_tokens": response.usage.total_tokens,
    }
    return {
        "content": response.choices[0].message.content,
        "usage": usage,
        "model": response.model,
        "id": response.id,
        "finish_reason": response.choices[0].finish_reason,
    }
