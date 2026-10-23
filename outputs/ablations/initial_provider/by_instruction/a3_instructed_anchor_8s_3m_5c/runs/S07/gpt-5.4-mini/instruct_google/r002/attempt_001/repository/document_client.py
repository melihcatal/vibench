import os
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class DocumentClientConfig:
    gcp_project_id: Optional[str] = None
    gcp_location: str = "us"
    gcp_processor_id: Optional[str] = None
    gcp_ocr_processor_id: Optional[str] = None
    gcp_layout_processor_id: Optional[str] = None
    gcp_form_processor_id: Optional[str] = None


def load_config() -> DocumentClientConfig:
    return DocumentClientConfig(
        gcp_project_id=os.getenv("GOOGLE_CLOUD_PROJECT"),
        gcp_location=os.getenv("GOOGLE_CLOUD_LOCATION", "us"),
        gcp_processor_id=os.getenv("GOOGLE_DOCUMENT_AI_PROCESSOR_ID"),
        gcp_ocr_processor_id=os.getenv("GOOGLE_DOCUMENT_AI_OCR_PROCESSOR_ID"),
        gcp_layout_processor_id=os.getenv("GOOGLE_DOCUMENT_AI_LAYOUT_PROCESSOR_ID"),
        gcp_form_processor_id=os.getenv("GOOGLE_DOCUMENT_AI_FORM_PROCESSOR_ID"),
    )


def build_documentai_name(project_id: str, location: str, processor_id: str) -> str:
    return f"projects/{project_id}/locations/{location}/processors/{processor_id}"


def provider_metadata() -> Dict[str, Any]:
    return {"provider": "google", "api": "documentai.googleapis.com", "sdk": "google-cloud-documentai"}
