import os
from dataclasses import dataclass


@dataclass
class DocumentClientConfig:
    endpoint: str | None = None
    key: str | None = None
    model_id: str | None = None


def load_config() -> DocumentClientConfig:
    return DocumentClientConfig(
        endpoint=os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"),
        key=os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY"),
        model_id=os.getenv("AZURE_DOCUMENT_INTELLIGENCE_MODEL_ID", "prebuilt-layout"),
    )


def require_config() -> DocumentClientConfig:
    cfg = load_config()
    if not cfg.endpoint or not cfg.key:
        raise ValueError(
            "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY are required"
        )
    return cfg
