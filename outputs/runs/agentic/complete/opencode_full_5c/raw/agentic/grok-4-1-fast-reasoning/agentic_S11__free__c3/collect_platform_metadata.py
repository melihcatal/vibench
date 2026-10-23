from typing import Any, Dict, Optional

from .model_models import Usage, PlatformMetadata


def collect_platform_metadata(response: Any) -> Dict[str, Any]:
    choice = response.choices[0]
    content = choice.message.content
    usage_data = response.usage
    usage = {
        "prompt_tokens": usage_data.prompt_tokens if usage_data else 0,
        "completion_tokens": usage_data.completion_tokens if usage_data else 0,
        "total_tokens": usage_data.total_tokens if usage_data else 0,
    }
    metadata: PlatformMetadata = {
        "request_id": response.id,
        "system_fingerprint": getattr(response, "system_fingerprint", None),
        "finish_reason": choice.finish_reason,
        "usage": usage,
    }
    return {"output": content, "metadata": metadata}
