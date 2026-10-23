from model_client import get_platform_client, get_default_deployment
from model_models import PlatformMetadata, Usage
import openai
from typing import Dict, Any


def collect_platform_metadata(prompt: str, model: str = None) -> PlatformMetadata:
    from invoke_platform_model import invoke_platform_model

    full_response = invoke_platform_model(prompt, model)
    content = full_response.choices[0].message.content or ""
    usage_data = full_response.usage.model_dump() if full_response.usage else None
    usage: Usage = (
        {
            "prompt_tokens": usage_data["prompt_tokens"] if usage_data else 0,
            "completion_tokens": usage_data["completion_tokens"] if usage_data else 0,
            "total_tokens": usage_data["total_tokens"] if usage_data else 0,
        }
        if usage_data
        else None
    )
    return PlatformMetadata(
        content=content,
        model=full_response.model,
        request_id=full_response.id,
        usage=usage,
    )
