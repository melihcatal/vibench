from typing import Iterable

from model_client import build_client, stream_complete
from model_models import PlatformRequest


def stream_platform_generation(
    prompt: str, model: str | None = None
) -> Iterable[object]:
    return stream_complete(build_client(), PlatformRequest(prompt=prompt, model=model))
