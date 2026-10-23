import base64
import os
from dataclasses import dataclass
from typing import Optional

from openai import OpenAI


@dataclass
class VisionConfig:
    api_key: Optional[str] = None
    model: str = "gpt-5.4-mini"
    base_url: Optional[str] = None


def load_vision_config() -> VisionConfig:
    return VisionConfig(
        api_key=os.getenv("OPENAI_API_KEY"),
        model=os.getenv("OPENAI_VISION_MODEL", "gpt-5.4-mini"),
        base_url=os.getenv("OPENAI_BASE_URL"),
    )


def get_client(config: Optional[VisionConfig] = None) -> OpenAI:
    cfg = config or load_vision_config()
    kwargs = {"api_key": cfg.api_key}
    if cfg.base_url:
        kwargs["base_url"] = cfg.base_url
    return OpenAI(**kwargs)


def image_data_url(image_path: str) -> str:
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("ascii")
    ext = image_path.rsplit(".", 1)[-1].lower()
    mime = "image/jpeg" if ext in {"jpg", "jpeg"} else f"image/{ext if ext in {'png', 'webp', 'gif'} else 'png'}"
    return f"data:{mime};base64,{encoded}"
