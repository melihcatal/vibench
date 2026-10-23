import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import google.cloud.documentai_v1 as documentai


@dataclass
class DocumentClientConfig:
    project_id: str
    location: str
    processor_id: str
    mime_type: str = "application/pdf"


def load_config() -> DocumentClientConfig:
    return DocumentClientConfig(
        project_id=os.environ.get("GOOGLE_CLOUD_PROJECT", ""),
        location=os.environ.get("GOOGLE_DOCUMENT_AI_LOCATION", "us"),
        processor_id=os.environ.get("GOOGLE_DOCUMENT_AI_PROCESSOR_ID", ""),
        mime_type=os.environ.get("GOOGLE_DOCUMENT_AI_MIME_TYPE", "application/pdf"),
    )


def build_client() -> documentai.DocumentProcessorServiceClient:
    return documentai.DocumentProcessorServiceClient()


def processor_name(config: DocumentClientConfig) -> str:
    return f"projects/{config.project_id}/locations/{config.location}/processors/{config.processor_id}"


def document_bytes(payload: Any) -> bytes:
    if isinstance(payload, bytes):
        return payload
    if isinstance(payload, str) and os.path.exists(payload):
        with open(payload, "rb") as handle:
            return handle.read()
    if isinstance(payload, str):
        return payload.encode("utf-8")
    raise TypeError("Unsupported payload type")


def process_document(payload: Any, config: Optional[DocumentClientConfig] = None) -> Dict[str, Any]:
    cfg = config or load_config()
    client = build_client()
    raw_document = documentai.RawDocument(content=document_bytes(payload), mime_type=cfg.mime_type)
    request = documentai.ProcessRequest(name=processor_name(cfg), raw_document=raw_document)
    result = client.process_document(request=request)
    document = result.document
    return {
        "text": document.text,
        "entities": [
            {
                "type": entity.type_,
                "mention_text": entity.mention_text,
                "confidence": float(entity.confidence),
            }
            for entity in document.entities
        ],
    }
