import os
from dataclasses import dataclass


def _env(name: str, default: str = "") -> str:
    return os.getenv(name, default)


@dataclass(frozen=True)
class VisionConfig:
    api_key: str = _env("DASHSCOPE_API_KEY")
    model: str = _env("DASHSCOPE_VISION_MODEL", "qwen-vl-max")
    base_url: str = _env(
        "DASHSCOPE_BASE_URL",
        "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation",
    )


def load_config() -> VisionConfig:
    return VisionConfig()


def build_headers(config: VisionConfig) -> dict:
    return {
        "Authorization": f"Bearer {config.api_key}",
        "Content-Type": "application/json",
    }
