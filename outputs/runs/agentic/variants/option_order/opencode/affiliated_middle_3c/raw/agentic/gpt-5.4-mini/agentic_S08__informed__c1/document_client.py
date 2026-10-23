import os
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class DocumentClientConfig:
    azure_endpoint: str
    azure_key: str


def load_config() -> DocumentClientConfig:
    return DocumentClientConfig(
        azure_endpoint=os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT", ""),
        azure_key=os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY", ""),
    )


def ensure_config(
    config: Optional[DocumentClientConfig] = None,
) -> DocumentClientConfig:
    cfg = config or load_config()
    if not cfg.azure_endpoint or not cfg.azure_key:
        raise ValueError(
            "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY are required"
        )
    return cfg


def document_bytes(payload: Any) -> bytes:
    if isinstance(payload, bytes):
        return payload
    if isinstance(payload, str):
        with open(payload, "rb") as f:
            return f.read()
    if isinstance(payload, dict) and "content" in payload:
        content = payload["content"]
        return content if isinstance(content, bytes) else str(content).encode("utf-8")
    raise TypeError("Unsupported document payload")


def as_dict(value: Any) -> Dict[str, Any]:
    if isinstance(value, dict):
        return value
    if hasattr(value, "as_dict"):
        return value.as_dict()
    if hasattr(value, "to_dict"):
        return value.to_dict()
    return {"value": value}
