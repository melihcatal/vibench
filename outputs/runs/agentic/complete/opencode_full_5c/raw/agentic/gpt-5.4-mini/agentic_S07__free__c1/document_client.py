import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from google.cloud import documentai_v1 as documentai


@dataclass
class DocumentAIConfig:
    project_id: str
    location: str
    processor_id: str
    processor_version: Optional[str] = None


def load_config() -> DocumentAIConfig:
    return DocumentAIConfig(
        project_id=os.environ["GOOGLE_CLOUD_PROJECT"],
        location=os.environ.get("DOCUMENTAI_LOCATION", "us"),
        processor_id=os.environ["DOCUMENTAI_PROCESSOR_ID"],
        processor_version=os.environ.get("DOCUMENTAI_PROCESSOR_VERSION"),
    )


def create_client() -> documentai.DocumentProcessorServiceClient:
    return documentai.DocumentProcessorServiceClient()


def processor_name(config: DocumentAIConfig) -> str:
    return f"projects/{config.project_id}/locations/{config.location}/processors/{config.processor_id}"


def processor_version_name(config: DocumentAIConfig) -> Optional[str]:
    if not config.processor_version:
        return None
    return f"{processor_name(config)}/processorVersions/{config.processor_version}"


def process_bytes(
    client: documentai.DocumentProcessorServiceClient,
    config: DocumentAIConfig,
    content: bytes,
    mime_type: str = "image/png",
    skip_human_review: bool = True,
) -> documentai.Document:
    raw_document = documentai.RawDocument(content=content, mime_type=mime_type)
    request: Dict[str, Any] = {
        "name": processor_name(config),
        "raw_document": raw_document,
        "skip_human_review": skip_human_review,
    }
    version_name = processor_version_name(config)
    if version_name:
        request["processor_version"] = version_name
    response = client.process_document(request=request)
    return response.document
