from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from google.cloud import documentai

DEFAULT_PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "")
DEFAULT_LOCATION = os.getenv("DOCUMENTAI_LOCATION", "us")
DEFAULT_PROCESSOR_ID = os.getenv("DOCUMENTAI_PROCESSOR_ID", "")
DEFAULT_ENDPOINT = f"{DEFAULT_LOCATION}-documentai.googleapis.com"


@dataclass(frozen=True)
class DocumentAiConfig:
    project_id: str = DEFAULT_PROJECT_ID
    location: str = DEFAULT_LOCATION
    processor_id: str = DEFAULT_PROCESSOR_ID
    endpoint: str = DEFAULT_ENDPOINT

    @property
    def processor_name(self) -> str:
        return documentai.DocumentProcessorServiceClient.processor_path(
            self.project_id, self.location, self.processor_id
        )


def build_document_ai_client(endpoint: Optional[str] = None) -> documentai.DocumentProcessorServiceClient:
    client_options = {"api_endpoint": endpoint or DEFAULT_ENDPOINT}
    return documentai.DocumentProcessorServiceClient(client_options=client_options)


def build_process_request(image_bytes: bytes, mime_type: str = "image/png", config: Optional[DocumentAiConfig] = None) -> Dict[str, Any]:
    cfg = config or DocumentAiConfig()
    return {
        "name": cfg.processor_name,
        "raw_document": {
            "content": image_bytes,
            "mime_type": mime_type,
        },
    }
