import os
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class DocumentClientConfig:
    project_id: Optional[str] = None
    location: Optional[str] = None
    processor_id: Optional[str] = None
    credentials_path: Optional[str] = None


def load_document_config() -> DocumentClientConfig:
    return DocumentClientConfig(
        project_id=os.getenv("GOOGLE_CLOUD_PROJECT"),
        location=os.getenv("DOCUMENT_AI_LOCATION", "us"),
        processor_id=os.getenv("DOCUMENT_AI_PROCESSOR_ID"),
        credentials_path=os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
    )


def document_ai_processor_name(config: DocumentClientConfig) -> str:
    if not config.project_id or not config.location or not config.processor_id:
        raise ValueError("Missing Document AI configuration")
    return f"projects/{config.project_id}/locations/{config.location}/processors/{config.processor_id}"


def normalize_structured_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in payload.items() if v is not None}
