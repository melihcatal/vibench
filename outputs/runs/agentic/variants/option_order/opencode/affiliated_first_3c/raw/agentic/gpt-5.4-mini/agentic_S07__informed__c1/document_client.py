import os
from dataclasses import dataclass
from typing import Optional


def _env(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.getenv(name, default)
    return value if value else default


@dataclass
class DocumentServiceConfig:
    endpoint: str
    key: str
    api_version: str = "2024-02-29-preview"


def load_document_service_config() -> DocumentServiceConfig:
    endpoint = _env("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT", "")
    key = _env("AZURE_DOCUMENT_INTELLIGENCE_KEY", "")
    if not endpoint or not key:
        raise ValueError(
            "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY are required"
        )
    return DocumentServiceConfig(endpoint=endpoint.rstrip("/"), key=key)


def build_client_kwargs(config: Optional[DocumentServiceConfig] = None) -> dict:
    cfg = config or load_document_service_config()
    return {
        "endpoint": cfg.endpoint,
        "credential": cfg.key,
        "api_version": cfg.api_version,
    }
