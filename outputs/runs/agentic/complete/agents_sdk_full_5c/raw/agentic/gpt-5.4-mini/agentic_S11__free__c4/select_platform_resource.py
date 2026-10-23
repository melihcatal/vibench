from __future__ import annotations

from typing import Optional

from google.cloud import aiplatform

from model_client import init_vertex_ai, load_config


def select_platform_resource(resource_name: Optional[str] = None):
    config = init_vertex_ai()
    name = resource_name or config.vertex_ai_endpoint or f"projects/{config.project}/locations/{config.location}/publishers/google/models/{config.model_name}"
    if "/endpoints/" in name:
        return aiplatform.Endpoint(endpoint_name=name)
    return name
