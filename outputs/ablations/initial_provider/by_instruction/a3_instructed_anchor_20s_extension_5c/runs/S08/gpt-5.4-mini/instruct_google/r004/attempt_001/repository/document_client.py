import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from google.cloud import documentai


@dataclass
class DocumentClientConfig:
    project_id: str
    location: str
    processor_id: str


def load_config(prefix: str = "GOOGLE_DOCUMENTAI_") -> DocumentClientConfig:
    return DocumentClientConfig(
        project_id=os.environ[f"{prefix}PROJECT_ID"],
        location=os.environ.get(f"{prefix}LOCATION", "us"),
        processor_id=os.environ[f"{prefix}PROCESSOR_ID"],
    )


def get_client() -> documentai.DocumentProcessorServiceClient:
    return documentai.DocumentProcessorServiceClient()


def processor_path(config: DocumentClientConfig) -> str:
    return f"projects/{config.project_id}/locations/{config.location}/processors/{config.processor_id}"


def process_content(client: documentai.DocumentProcessorServiceClient, config: DocumentClientConfig, content: bytes, mime_type: str) -> Any:
    request = documentai.ProcessRequest(
        name=processor_path(config),
        raw_document=documentai.RawDocument(content=content, mime_type=mime_type),
    )
    return client.process_document(request=request).document


def entity_to_dict(entity: Any) -> Dict[str, Any]:
    properties = [entity_to_dict(prop) for prop in getattr(entity, "properties", [])]
    return {
        "type": getattr(entity, "type_", ""),
        "mention_text": getattr(entity, "mention_text", ""),
        "normalized_value": getattr(getattr(entity, "normalized_value", None), "text", ""),
        "confidence": float(getattr(entity, "confidence", 0.0) or 0.0),
        "properties": properties,
    }
