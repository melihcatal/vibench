import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from google.cloud import documentai_v1 as documentai


@dataclass
class DocumentAIConfig:
    project_id: str
    location: str = "us"
    processor_id: Optional[str] = None

    @classmethod
    def from_env(cls) -> "DocumentAIConfig":
        return cls(
            project_id=os.getenv("GOOGLE_CLOUD_PROJECT", ""),
            location=os.getenv("DOCUMENTAI_LOCATION", "us"),
            processor_id=os.getenv("DOCUMENTAI_PROCESSOR_ID"),
        )


class DocumentAIClientHelper:
    def __init__(self, config: Optional[DocumentAIConfig] = None):
        self.config = config or DocumentAIConfig.from_env()
        self.client = documentai.DocumentProcessorServiceClient()

    def processor_name(self) -> str:
        if not self.config.processor_id:
            raise ValueError("DOCUMENTAI_PROCESSOR_ID is required")
        return self.client.processor_path(
            self.config.project_id, self.config.location, self.config.processor_id
        )

    def process_document(self, content: bytes, mime_type: str = "application/pdf") -> Dict[str, Any]:
        raw_document = documentai.RawDocument(content=content, mime_type=mime_type)
        request = documentai.ProcessRequest(
            name=self.processor_name(),
            raw_document=raw_document,
        )
        result = self.client.process_document(request=request)
        return documentai.Document.to_dict(result.document)


def load_documentai_client() -> DocumentAIClientHelper:
    return DocumentAIClientHelper()
