from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Optional

from google.cloud import documentai

from document_models import DocumentRequest


@dataclass
class DocumentClientConfig:
    project_id: Optional[str] = None
    location: str = "us"
    processor_id: Optional[str] = None
    mime_type: str = "image/png"

    @classmethod
    def from_env(cls) -> "DocumentClientConfig":
        return cls(
            project_id=os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT"),
            location=os.getenv("DOCUMENT_AI_LOCATION", "us"),
            processor_id=os.getenv("DOCUMENT_AI_PROCESSOR_ID"),
            mime_type=os.getenv("DOCUMENT_AI_MIME_TYPE", "image/png"),
        )


class DocumentAIClientHelper:
    def __init__(self, config: Optional[DocumentClientConfig] = None) -> None:
        self.config = config or DocumentClientConfig.from_env()
        self.client = documentai.DocumentProcessorServiceClient()

    def processor_name(self) -> str:
        if not self.config.project_id or not self.config.processor_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT and DOCUMENT_AI_PROCESSOR_ID are required")
        return self.client.processor_path(self.config.project_id, self.config.location, self.config.processor_id)

    def raw_document_from_request(self, request: DocumentRequest) -> documentai.RawDocument:
        if request.file_bytes is not None:
            content = request.file_bytes
        elif request.file_path:
            with open(request.file_path, "rb") as handle:
                content = handle.read()
        else:
            raise ValueError("DocumentRequest requires file_path or file_bytes")
        return documentai.RawDocument(content=content, mime_type=request.mime_type or self.config.mime_type)

    def process(self, request: DocumentRequest) -> Any:
        raw_document = self.raw_document_from_request(request)
        doc_request = documentai.ProcessRequest(name=self.processor_name(), raw_document=raw_document)
        return self.client.process_document(request=doc_request)
