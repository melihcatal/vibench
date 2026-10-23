import os
from typing import Any, Dict, Optional

from model_client import build_platform_client, get_config
from model_models import PlatformInvocationRequest, coerce_text


def invoke_platform_model(prompt: str, resource_id: Optional[str] = None, **kwargs: Any) -> Dict[str, Any]:
    config = get_config()
    client = build_platform_client(config)
    request = PlatformInvocationRequest(prompt=prompt, resource_id=resource_id, extra=kwargs)
    if config.provider == "openai":
        response = client.responses.create(
            model=request.resource_id or config.model_id,
            input=request.prompt,
            **request.extra,
        )
        return {"text": coerce_text(response), "response": response}
    if config.provider == "anthropic":
        response = client.messages.create(
            model=request.resource_id or config.model_id,
            max_tokens=request.extra.pop("max_tokens", config.max_tokens),
            messages=[{"role": "user", "content": request.prompt}],
            **request.extra,
        )
        return {"text": coerce_text(response), "response": response}
    raise RuntimeError(f"Unsupported provider: {config.provider}")
