from __future__ import annotations

import os
from typing import Optional

import vertexai
from vertexai.generative_models import GenerativeModel

from model_models import PlatformRequest, PlatformResource


DEFAULT_VERTEX_MODEL = "gemini-1.5-pro"


def get_vertex_project_id() -> str:
    return os.environ["VERTEX_PROJECT_ID"]


def get_vertex_location() -> str:
    return os.getenv("VERTEX_LOCATION", "us-central1")


def initialize_vertex_ai(
    project_id: Optional[str] = None, location: Optional[str] = None
) -> None:
    vertexai.init(
        project=project_id or get_vertex_project_id(),
        location=location or get_vertex_location(),
    )


def resolve_vertex_resource(model_name: Optional[str] = None) -> PlatformResource:
    return PlatformResource(
        project_id=get_vertex_project_id(),
        location=get_vertex_location(),
        publisher="google",
        model=model_name or os.getenv("VERTEX_MODEL", DEFAULT_VERTEX_MODEL),
    )


def get_vertex_model(resource: PlatformResource) -> GenerativeModel:
    initialize_vertex_ai(resource.project_id, resource.location)
    return GenerativeModel(resource.full_model_name)


def generation_config_from_request(request: PlatformRequest) -> dict:
    return {
        "max_output_tokens": request.max_tokens,
        "temperature": request.temperature,
        "top_p": request.top_p,
    }
