from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional, Sequence

from google.cloud import documentai_v1 as documentai


@dataclass
class FieldExtractionConfig:
    project_id: Optional[str] = None
    location: str = "us"
    processor_id: Optional[str] = None
    timeout: float = 60.0

    @classmethod
    def from_env(cls) -> "FieldExtractionConfig":
        return cls(
            project_id=os.getenv("GOOGLE_CLOUD_PROJECT"),
            location=os.getenv("DOCUMENTAI_LOCATION", "us"),
            processor_id=os.getenv("DOCUMENTAI_PROCESSOR_ID"),
            timeout=float(os.getenv("DOCUMENTAI_TIMEOUT", "60")),
        )


@dataclass
class ExtractedField:
    name: str
    value: str
    confidence: Optional[float] = None
    normalized_value: Optional[str] = None
    page: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {"name": self.name, "value": self.value}
        if self.confidence is not None:
            data["confidence"] = self.confidence
        if self.normalized_value is not None:
            data["normalized_value"] = self.normalized_value
        if self.page is not None:
            data["page"] = self.page
        if self.metadata:
            data.update(self.metadata)
        return data


def _processor_path(project_id: str, location: str, processor_id: str) -> str:
    return f"projects/{project_id}/locations/{location}/processors/{processor_id}"


def _get_client() -> documentai.DocumentProcessorServiceClient:
    return documentai.DocumentProcessorServiceClient()


def _entities_to_fields(entities: Iterable[Any]) -> List[ExtractedField]:
    fields: List[ExtractedField] = []
    for entity in entities:
        name = str(getattr(entity, "type_", "") or getattr(entity, "type", "") or "")
        value = str(getattr(entity, "mention_text", "") or "")
        confidence = getattr(entity, "confidence", None)
        normalized_value = getattr(entity, "normalized_value", None)
        if normalized_value is not None and not isinstance(normalized_value, str):
            normalized_value = str(normalized_value)
        page = getattr(entity, "page_anchor", None)
        metadata: Dict[str, Any] = {}
        for key in ("id", "mention_id"):
            val = getattr(entity, key, None)
            if val is not None:
                metadata[key] = val
        if page is not None:
            metadata["page_anchor"] = page
        fields.append(
            ExtractedField(
                name=name,
                value=value,
                confidence=float(confidence) if confidence is not None else None,
                normalized_value=normalized_value,
                metadata=metadata,
            )
        )
    return fields


def extract_fields_from_text(
    text: str,
    *,
    mime_type: str = "text/plain",
    config: Optional[FieldExtractionConfig] = None,
    project_id: Optional[str] = None,
    location: Optional[str] = None,
    processor_id: Optional[str] = None,
) -> List[Dict[str, Any]]:
    config = config or FieldExtractionConfig.from_env()
    project_id = project_id or config.project_id or os.environ["GOOGLE_CLOUD_PROJECT"]
    location = location or config.location
    processor_id = processor_id or config.processor_id or os.environ["DOCUMENTAI_PROCESSOR_ID"]

    client = _get_client()
    name = _processor_path(project_id, location, processor_id)
    raw_document = documentai.RawDocument(content=text.encode("utf-8"), mime_type=mime_type)
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_document(request=request)
    document = result.document
    return [field.to_dict() for field in _entities_to_fields(document.entities)]


def extract_fields_from_bytes(
    content: bytes,
    mime_type: str,
    *,
    config: Optional[FieldExtractionConfig] = None,
    project_id: Optional[str] = None,
    location: Optional[str] = None,
    processor_id: Optional[str] = None,
) -> List[Dict[str, Any]]:
    config = config or FieldExtractionConfig.from_env()
    project_id = project_id or config.project_id or os.environ["GOOGLE_CLOUD_PROJECT"]
    location = location or config.location
    processor_id = processor_id or config.processor_id or os.environ["DOCUMENTAI_PROCESSOR_ID"]

    client = _get_client()
    name = _processor_path(project_id, location, processor_id)
    raw_document = documentai.RawDocument(content=content, mime_type=mime_type)
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_document(request=request)
    document = result.document
    return [field.to_dict() for field in _entities_to_fields(document.entities)]


def extract_fields_from_uri(
    gcs_uri: str,
    mime_type: str,
    *,
    config: Optional[FieldExtractionConfig] = None,
    project_id: Optional[str] = None,
    location: Optional[str] = None,
    processor_id: Optional[str] = None,
) -> List[Dict[str, Any]]:
    config = config or FieldExtractionConfig.from_env()
    project_id = project_id or config.project_id or os.environ["GOOGLE_CLOUD_PROJECT"]
    location = location or config.location
    processor_id = processor_id or config.processor_id or os.environ["DOCUMENTAI_PROCESSOR_ID"]

    client = _get_client()
    name = _processor_path(project_id, location, processor_id)
    gcs_document = documentai.GcsDocument(gcs_uri=gcs_uri, mime_type=mime_type)
    input_config = documentai.InputConfig(gcs_documents=documentai.GcsDocuments(documents=[gcs_document]))
    request = documentai.ProcessRequest(name=name, input_documents=input_config)
    result = client.process_document(request=request)
    document = result.document
    return [field.to_dict() for field in _entities_to_fields(document.entities)]
