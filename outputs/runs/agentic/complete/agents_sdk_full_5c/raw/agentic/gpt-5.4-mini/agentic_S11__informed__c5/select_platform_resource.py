from __future__ import annotations

from typing import Optional

from vertexai.generative_models import GenerativeModel

from model_client import load_platform_config


def select_platform_resource(model_name: Optional[str] = None) -> GenerativeModel:
    config = load_platform_config()
    chosen_model = model_name or config.model_name
    return GenerativeModel(chosen_model)
