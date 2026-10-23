from __future__ import annotations

import os
from typing import Any, Dict, Iterator, Optional, Tuple

from openai import OpenAI


def _build_client(api_key: Optional[str] = None) -> OpenAI:
    return OpenAI(api_key=api_key or os.environ.get("OPENAI_API_KEY"))


def stream_platform_generation(
    prompt: str,
    *,
    model: str = "gpt-5.4-mini",
    api_key: Optional[str] = None,
    **kwargs: Any,
) -> Tuple[Iterator[Any], Any]:
    client = _build_client(api_key)
    response = client.responses.stream(model=model, input=prompt, **kwargs)

    def iterator() -> Iterator[Any]:
        with response as stream:
            for event in stream:
                yield event

    return iterator(), response
