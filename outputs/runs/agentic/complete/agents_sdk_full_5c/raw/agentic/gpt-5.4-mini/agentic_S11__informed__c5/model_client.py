from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class PlatformConfig:
    project_id: str
    location: str
    model_name: str


def load_platform_config() -> PlatformConfig:
    return PlatformConfig(
        project_id=os.getenv("GOOGLE_CLOUD_PROJECT", os.getenv("GCP_PROJECT", "demo-project")),
        location=os.getenv("VERTEX_AI_LOCATION", "us-central1"),
        model_name=os.getenv("VERTEX_AI_MODEL", "gemini-1.5-pro"),
    )


def build_vertex_model():
    from vertexai.generative_models import GenerativeModel

    config = load_platform_config()
    return GenerativeModel(config.model_name)


def build_vertex_prompt(prompt: str, system_instruction: Optional[str] = None) -> str:
    if system_instruction:
        return f"{system_instruction}\n\n{prompt}"
    return prompt
