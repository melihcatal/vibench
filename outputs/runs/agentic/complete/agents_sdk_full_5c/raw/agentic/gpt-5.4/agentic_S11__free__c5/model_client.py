from __future__ import annotations

import os
from typing import Optional

import vertexai
from vertexai.generative_models import GenerativeModel
from google.cloud import aiplatform_v1

from model_models import PlatformSelection


DEFAULT_MODEL = os.getenv("VERTEX_MODEL", "gemini-1.5-pro")
DEFAULT_LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
DEFAULT_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", "")



def get_project_id(explicit: Optional[str] = None) -> str:
    project_id = explicit or DEFAULT_PROJECT
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT is required for Vertex AI")
    return project_id



def get_location(explicit: Optional[str] = None) -> str:
    return explicit or DEFAULT_LOCATION



def init_vertex(project_id: Optional[str] = None, location: Optional[str] = None) -> tuple[str, str]:
    resolved_project = get_project_id(project_id)
    resolved_location = get_location(location)
    vertexai.init(project=resolved_project, location=resolved_location)
    return resolved_project, resolved_location



def default_selection(project_id: Optional[str] = None, location: Optional[str] = None) -> PlatformSelection:
    project, region = init_vertex(project_id=project_id, location=location)
    return PlatformSelection(project_id=project, location=region, model=DEFAULT_MODEL)



def get_model(model_name: Optional[str] = None, project_id: Optional[str] = None, location: Optional[str] = None) -> GenerativeModel:
    init_vertex(project_id=project_id, location=location)
    return GenerativeModel(model_name or DEFAULT_MODEL)



def prediction_service_client(api_endpoint: Optional[str] = None) -> aiplatform_v1.PredictionServiceClient:
    endpoint = api_endpoint or f"{DEFAULT_LOCATION}-aiplatform.googleapis.com"
    return aiplatform_v1.PredictionServiceClient(client_options={"api_endpoint": endpoint})
