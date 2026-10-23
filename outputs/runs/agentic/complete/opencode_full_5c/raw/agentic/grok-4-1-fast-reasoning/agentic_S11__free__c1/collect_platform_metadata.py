from model_client import get_platform_client
from typing import Dict, Any


def collect_platform_metadata(prompt: str, deployment_id: str) -> Dict[str, Any]:
    """
    Collects model output with Azure OpenAI platform metadata like usage and resource IDs.
    """
    client = get_platform_client()
    response = client.chat.completions.create(
        model=deployment_id,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024,
    )
    usage = None
    if response.usage:
        usage = {
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens,
        }
    return {
        "content": response.choices[0].message.content,
        "model": response.model,
        "usage": usage,
        "finish_reason": response.choices[0].finish_reason,
        "resource_id": deployment_id,
    }
