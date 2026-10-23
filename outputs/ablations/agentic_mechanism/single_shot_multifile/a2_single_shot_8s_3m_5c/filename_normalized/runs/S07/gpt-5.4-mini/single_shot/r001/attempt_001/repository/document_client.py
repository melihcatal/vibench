import os
from functools import lru_cache
from google.cloud import vision
from google.cloud import documentai


@lru_cache(maxsize=1)
def get_vision_client() -> vision.ImageAnnotatorClient:
    return vision.ImageAnnotatorClient()


@lru_cache(maxsize=1)
def get_document_ai_client() -> documentai.DocumentProcessorServiceClient:
    return documentai.DocumentProcessorServiceClient()


def get_document_ai_processor_name(processor_id: str, location: str, project_id: str | None = None) -> str:
    project = project_id or os.getenv("GOOGLE_CLOUD_PROJECT", "")
    return f"projects/{project}/locations/{location}/processors/{processor_id}"
