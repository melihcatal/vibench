import os
from dataclasses import dataclass

from google.cloud import vision


@dataclass
class DocumentClientConfig:
    project_id: str | None = None
    location: str | None = None
    processor_id: str | None = None


def load_config() -> DocumentClientConfig:
    return DocumentClientConfig(
        project_id=os.getenv("GOOGLE_CLOUD_PROJECT"),
        location=os.getenv("GOOGLE_CLOUD_LOCATION", "us"),
        processor_id=os.getenv("GOOGLE_DOCAI_PROCESSOR_ID"),
    )


def vision_client() -> vision.ImageAnnotatorClient:
    return vision.ImageAnnotatorClient()


def normalize_text(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.splitlines()).strip()


def normalize_kv_pairs(pairs):
    normalized = {}
    for item in pairs or []:
        if isinstance(item, dict) and "key" in item and "value" in item:
            normalized[str(item["key"])] = str(item["value"])
    return normalized
