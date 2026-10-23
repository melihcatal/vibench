from typing import Any, Dict, Iterator, Optional

from model_client import build_platform_client, get_config
from model_models import PlatformStreamChunk, coerce_text


def stream_platform_generation(prompt: str, resource_id: Optional[str] = None, **kwargs: Any) -> Iterator[Dict[str, Any]]:
    config = get_config()
    client = build_platform_client(config)
    if config.provider == "openai":
        stream = client.responses.create(
            model=resource_id or config.model_id,
            input=prompt,
            stream=True,
            **kwargs,
        )
        for event in stream:
            yield {"chunk": PlatformStreamChunk(provider="openai", raw=event, text=coerce_text(event)).to_dict()}
        return
    if config.provider == "anthropic":
        stream = client.messages.create(
            model=resource_id or config.model_id,
            max_tokens=kwargs.pop("max_tokens", config.max_tokens),
            messages=[{"role": "user", "content": prompt}],
            stream=True,
            **kwargs,
        )
        for event in stream:
            yield {"chunk": PlatformStreamChunk(provider="anthropic", raw=event, text=coerce_text(event)).to_dict()}
        return
    raise RuntimeError(f"Unsupported provider: {config.provider}")
