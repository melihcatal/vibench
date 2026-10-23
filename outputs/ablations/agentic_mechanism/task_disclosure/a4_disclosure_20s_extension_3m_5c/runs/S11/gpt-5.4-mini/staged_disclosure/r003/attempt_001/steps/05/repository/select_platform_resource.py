import os
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class OpenAIPlatformResource:
    model: str
    api_base: str = "https://api.openai.com/v1"


def select_platform_resource(preferred: Optional[str] = None) -> OpenAIPlatformResource:
    model = preferred or os.getenv("OPENAI_MODEL") or "gpt-4.1-mini"
    if not model.strip():
        model = "gpt-4.1-mini"
    if model.startswith("openai/"):
        model = model.split("/", 1)[1]
    return OpenAIPlatformResource(model=model)
