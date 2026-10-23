from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

from google.cloud import aiplatform


@dataclass(frozen=True)
class PlatformConfig:
    project: str
    location: str
    vertex_ai_endpoint: Optional[str] = None
    model_name: str = "gemini-1.5-pro"


@lru_cache(maxsize=1)
def load_config() -> PlatformConfig:
    project = os.environ["GOOGLE_CLOUD_PROJECT"]
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    endpoint = os.getenv("VERTEX_AI_ENDPOINT")
    model_name = os.getenv("VERTEX_AI_MODEL", "gemini-1.5-pro")
    return PlatformConfig(project=project, location=location, vertex_ai_endpoint=endpoint, model_name=model_name)


def init_vertex_ai() -> PlatformConfig:
    config = load_config()
    aiplatform.init(project=config.project, location=config.location)
    return config


def build_model_name(config: Optional[PlatformConfig] = None) -> str:
    cfg = config or load_config()
    return cfg.model_name
