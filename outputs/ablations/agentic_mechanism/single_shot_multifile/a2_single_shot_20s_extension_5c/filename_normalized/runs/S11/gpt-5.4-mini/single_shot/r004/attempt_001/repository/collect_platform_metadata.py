from typing import Any, Dict, Optional

from model_client import build_platform_client, get_config
from model_models import collect_usage, coerce_text



def collect_platform_metadata(prompt: str, resource_id: Optional[str] = None, **kwargs: Any) -> Dict[str, Any]:
    config = get_config()
    client = build_platform_client(config)
    if config.provider == "openai":
        response = client.responses.create(
            model=resource_id or config.model_id,
            input=prompt,
            **kwargs,
        )
        return {
            "text": coerce_text(response),
            "usage": collect_usage(response),
            "provider": "openai",
            "resource_id": resource_id or config.model_id,
            "response": response,
        }
    if config.provider == "anthropic":
        response = client.messages.create(
            model=resource_id or config.model_id,
            max_tokens=kwargs.pop("max_tokens", config.max_tokens),
            messages=[{"role": "user", "content": prompt}],
            **kwargs,
        )
        return {
            "text": coerce_text(response),
            "usage": collect_usage(response),
            "provider": "anthropic",
            "resource_id": resource_id or config.model_id,
            "response": response,
        }
    raise RuntimeError(f"Unsupported provider: {config.provider}")
