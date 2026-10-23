import os
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class DocumentClientConfig:
    api_key: Optional[str] = None
    endpoint: Optional[str] = None
    processor_id: Optional[str] = None
    locale: Optional[str] = None


def load_document_client_config() -> DocumentClientConfig:
    return DocumentClientConfig(
        api_key=os.getenv("MINDEE_API_KEY")
        or os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")
        or os.getenv("GOOGLE_API_KEY"),
        endpoint=os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
        or os.getenv("MINDEE_ENDPOINT"),
        processor_id=os.getenv("DOCUMENT_PROCESSOR_ID")
        or os.getenv("MINDEE_PROCESSOR_ID"),
        locale=os.getenv("DOCUMENT_LOCALE", "en-US"),
    )


def normalize_document_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in payload.items() if v is not None}


def merge_confidence(*values: Optional[float]) -> float:
    scores = [v for v in values if isinstance(v, (int, float))]
    return float(sum(scores) / len(scores)) if scores else 0.0
