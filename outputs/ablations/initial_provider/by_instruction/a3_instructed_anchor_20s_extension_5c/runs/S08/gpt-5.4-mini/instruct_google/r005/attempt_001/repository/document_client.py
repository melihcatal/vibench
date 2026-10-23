import os
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class DocumentServiceConfig:
    project_id: str
    location: str = "us"
    processor_id: str = ""
    google_api_key: str = ""


def load_config() -> DocumentServiceConfig:
    return DocumentServiceConfig(
        project_id=os.getenv("GOOGLE_CLOUD_PROJECT", ""),
        location=os.getenv("GOOGLE_CLOUD_LOCATION", "us"),
        processor_id=os.getenv("GOOGLE_DOCUMENT_AI_PROCESSOR_ID", ""),
        google_api_key=os.getenv("GOOGLE_API_KEY", ""),
    )


def build_document_ai_endpoint(config: DocumentServiceConfig) -> str:
    return f"https://{config.location}-documentai.googleapis.com/v1/projects/{config.project_id}/locations/{config.location}/processors/{config.processor_id}:process"


def process_document_with_google_document_ai(payload: Dict[str, Any], config: Optional[DocumentServiceConfig] = None) -> Dict[str, Any]:
    cfg = config or load_config()
    return {
        "provider": "google-document-ai",
        "endpoint": build_document_ai_endpoint(cfg),
        "request": payload,
        "processor_id": cfg.processor_id,
    }
