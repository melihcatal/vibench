from __future__ import annotations

import os

from google.cloud import aiplatform_v1
from vertexai import init as vertexai_init
from vertexai.generative_models import GenerativeModel

from model_models import PlatformSelection


DEFAULT_PUBLISHER_MODEL = os.getenv("VERTEXAI_MODEL", "gemini-1.5-pro")
DEFAULT_LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
DEFAULT_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", "")



def load_platform_selection() -> PlatformSelection:
    project_id = DEFAULT_PROJECT
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT is required for Vertex AI")
    return PlatformSelection(
        project_id=project_id,
        location=DEFAULT_LOCATION,
        publisher_model=DEFAULT_PUBLISHER_MODEL,
        endpoint=os.getenv("VERTEXAI_ENDPOINT"),
    )



def init_vertexai(selection: PlatformSelection) -> None:
    vertexai_init(project=selection.project_id, location=selection.location)



def build_generative_model(selection: PlatformSelection) -> GenerativeModel:
    init_vertexai(selection)
    return GenerativeModel(selection.publisher_model)



def prediction_service_client(selection: PlatformSelection) -> aiplatform_v1.PredictionServiceClient:
    api_endpoint = selection.endpoint or f"{selection.location}-aiplatform.googleapis.com"
    return aiplatform_v1.PredictionServiceClient(
        client_options={"api_endpoint": api_endpoint}
    )
