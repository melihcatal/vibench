import base64
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from openai import OpenAI


def _env(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.getenv(name)
    return value if value not in (None, "") else default


@dataclass
class VisionConfig:
    openai_api_key: Optional[str] = None
    openai_base_url: Optional[str] = None
    analysis_model: str = "gpt-4.1-mini"
    translation_model: str = "gpt-4.1-mini"
    storage_bucket: Optional[str] = None
    storage_region: Optional[str] = None


def load_config() -> VisionConfig:
    return VisionConfig(
        openai_api_key=_env("OPENAI_API_KEY"),
        openai_base_url=_env("OPENAI_BASE_URL"),
        analysis_model=_env("OPENAI_VISION_MODEL", "gpt-4.1-mini"),
        translation_model=_env("OPENAI_TRANSLATION_MODEL", "gpt-4.1-mini"),
        storage_bucket=_env("AWS_S3_BUCKET"),
        storage_region=_env("AWS_REGION", _env("AWS_DEFAULT_REGION")),
    )


def get_openai_client(config: Optional[VisionConfig] = None) -> OpenAI:
    cfg = config or load_config()
    kwargs: Dict[str, Any] = {}
    if cfg.openai_api_key:
        kwargs["api_key"] = cfg.openai_api_key
    if cfg.openai_base_url:
        kwargs["base_url"] = cfg.openai_base_url
    return OpenAI(**kwargs)


def image_to_data_url(image_bytes: bytes, mime_type: str = "image/png") -> str:
    encoded = base64.b64encode(image_bytes).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def image_source(image: Any) -> Any:
    if isinstance(image, (bytes, bytearray)):
        return {"type": "input_image", "image_url": image_to_data_url(bytes(image))}
    if isinstance(image, str) and image.startswith("http"):
        return {"type": "input_image", "image_url": image}
    if isinstance(image, str):
        with open(image, "rb") as f:
            return {"type": "input_image", "image_url": image_to_data_url(f.read())}
    raise TypeError("Unsupported image input")
