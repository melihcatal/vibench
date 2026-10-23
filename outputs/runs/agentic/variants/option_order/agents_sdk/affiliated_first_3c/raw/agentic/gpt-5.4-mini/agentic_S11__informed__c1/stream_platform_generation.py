from __future__ import annotations

from typing import Iterable

from model_client import stream_model
from model_models import PlatformRequest


def stream(prompt: str, model: str) -> Iterable[object]:
    request = PlatformRequest(prompt=prompt, model=model)
    return stream_model(request)
