import os
from dataclasses import dataclass
from functools import lru_cache

from google.cloud import aiplatform


@dataclass(frozen=True)
class PlatformConfig:
    project: str
    location: str
    model_name: str
    safety_threshold: str


@lru_cache(maxsize=1)
def load_platform_config() -> PlatformConfig:
    return PlatformConfig(
        project=os.environ.get("GOOGLE_CLOUD_PROJECT", ""),
        location=os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1"),
        model_name=os.environ.get("VERTEX_MODEL_NAME", "gemini-1.5-pro-002"),
        safety_threshold=os.environ.get("VERTEX_SAFETY_THRESHOLD", "BLOCK_MEDIUM_AND_ABOVE"),
    )


def init_vertex_ai() -> PlatformConfig:
    config = load_platform_config()
    aiplatform.init(project=config.project, location=config.location)
    return config
