from __future__ import annotations

import os
from typing import Optional

import vertexai
from vertexai.generative_models import GenerativeModel

from model_models import PlatformSelection


DEFAULT_GEMINI_MODEL = os.getenv("VERTEXAI_MODEL", "gemini-1.5-pro")
DEFAULT_LOCATION = os.getenv("VERTEXAI_LOCATION", "us-central1")
DEFAULT_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", os.getenv("GCLOUD_PROJECT", ""))


def get_project_id(explicit: Optional[str] = None) -> str:
    project_id = explicit or DEFAULT_PROJECT
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT or GCLOUD_PROJECT must be set for Vertex AI")
    return project_id


def init_vertex_ai(project_id: Optional[str] = None, location: Optional[str] = None) -> tuple[str, str]:
    resolved_project = get_project_id(project_id)
    resolved_location = location or DEFAULT_LOCATION
    vertexai.init(project=resolved_project, location=resolved_location)
    return resolved_project, resolved_location


def build_selection(
    model_name: Optional[str] = None,
    project_id: Optional[str] = None,
    location: Optional[str] = None,
) -> PlatformSelection:
    resolved_project, resolved_location = init_vertex_ai(project_id=project_id, location=location)
    resolved_model = model_name or DEFAULT_GEMINI_MODEL
    publisher_model = f"projects/{resolved_project}/locations/{resolved_location}/publishers/google/models/{resolved_model}"
    endpoint = f"projects/{resolved_project}/locations/{resolved_location}/endpoints/openapi"
    return PlatformSelection(
        project_id=resolved_project,
        location=resolved_location,
        model_name=resolved_model,
        publisher_model=publisher_model,
        endpoint=endpoint,
    )


def get_generative_model(selection: PlatformSelection) -> GenerativeModel:
    init_vertex_ai(project_id=selection.project_id, location=selection.location)
    return GenerativeModel(selection.model_name)
