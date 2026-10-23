from __future__ import annotations

import os
from typing import Optional

from google.api_core.client_options import ClientOptions
from google.cloud import documentai_v1 as documentai


def get_project_id() -> str:
    return os.environ["GOOGLE_CLOUD_PROJECT"]


def get_location() -> str:
    return os.getenv("DOCUMENTAI_LOCATION", "us")


def get_processor_id(env_name: str) -> str:
    return os.environ[env_name]


def build_processor_name(processor_id: str) -> str:
    client = documentai.DocumentProcessorServiceClient(
        client_options=ClientOptions(api_endpoint=f"{get_location()}-documentai.googleapis.com")
    )
    return client.processor_path(get_project_id(), get_location(), processor_id)


def get_documentai_client() -> documentai.DocumentProcessorServiceClient:
    return documentai.DocumentProcessorServiceClient(
        client_options=ClientOptions(api_endpoint=f"{get_location()}-documentai.googleapis.com")
    )


def guess_mime_type(file_path: str, explicit: Optional[str] = None) -> str:
    if explicit:
        return explicit
    lower = file_path.lower()
    if lower.endswith(".pdf"):
        return "application/pdf"
    if lower.endswith(".png"):
        return "image/png"
    if lower.endswith(".jpg") or lower.endswith(".jpeg"):
        return "image/jpeg"
    if lower.endswith(".tif") or lower.endswith(".tiff"):
        return "image/tiff"
    return "application/octet-stream"
