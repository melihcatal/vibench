import os
from dataclasses import dataclass
from typing import Optional

from openai import OpenAI


@dataclass
class VisionConfig:
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    model: str = "gpt-4o-mini"
    storage_bucket: Optional[str] = None
    translation_model: str = "gpt-4.1-mini"


def load_config() -> VisionConfig:
    return VisionConfig(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL"),
        model=os.getenv("OPENAI_VISION_MODEL", "gpt-4o-mini"),
        storage_bucket=os.getenv("S3_BUCKET"),
        translation_model=os.getenv("OPENAI_TRANSLATION_MODEL", "gpt-4.1-mini"),
    )


def create_client(config: Optional[VisionConfig] = None) -> OpenAI:
    cfg = config or load_config()
    kwargs = {}
    if cfg.api_key:
        kwargs["api_key"] = cfg.api_key
    if cfg.base_url:
        kwargs["base_url"] = cfg.base_url
    return OpenAI(**kwargs)


def image_data_url(image_bytes: bytes, mime_type: str = "image/png") -> str:
    import base64

    encoded = base64.b64encode(image_bytes).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"
