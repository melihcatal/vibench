import os
from functools import lru_cache
from typing import Optional

from google.cloud import documentai

from document_models import DocumentRequest


DEFAULT_LOCATION = os.getenv("DOCUMENTAI_LOCATION", "us")
DEFAULT_PROCESSOR_ID = os.getenv("DOCUMENTAI_PROCESSOR_ID", "")
DEFAULT_PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", os.getenv("GCP_PROJECT", ""))


@lru_cache(maxsize=1)
def get_document_ai_client() -> documentai.DocumentProcessorServiceClient:
    return documentai.DocumentProcessorServiceClient()


def build_processor_name(project_id: Optional[str] = None, location: Optional[str] = None, processor_id: Optional[str] = None) -> str:
    project = project_id or DEFAULT_PROJECT_ID
    loc = location or DEFAULT_LOCATION
    proc = processor_id or DEFAULT_PROCESSOR_ID
    if not project or not proc:
        raise ValueError("Missing Google Cloud project or Document AI processor id")
    return f"projects/{project}/locations/{loc}/processors/{proc}"


def normalize_request(request: DocumentRequest) -> DocumentRequest:
    if request.content is None and not request.content_b64 and not request.gcs_uri:
        raise ValueError("DocumentRequest requires content, content_b64, or gcs_uri")
    return request
