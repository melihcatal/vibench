import os
from typing import Any, Dict, Iterator, Optional

from openai import OpenAI


def stream_platform_generation(
    prompt: str,
    model: str = "gpt-4.1-mini",
    api_key: Optional[str] = None,
) -> Iterator[Dict[str, Any]]:
    client = OpenAI(api_key=api_key or os.environ.get("OPENAI_API_KEY"))
    with client.responses.stream(model=model, input=prompt) as stream:
        for event in stream:
            yield {"provider": "openai", "event": event, "model": model}
