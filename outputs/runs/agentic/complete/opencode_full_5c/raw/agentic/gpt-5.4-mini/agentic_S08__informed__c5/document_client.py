import os
from dataclasses import dataclass


@dataclass
class DocumentServiceConfig:
    endpoint: str | None = None
    api_key: str | None = None
    api_version: str | None = None


def load_service_config(prefix: str) -> DocumentServiceConfig:
    return DocumentServiceConfig(
        endpoint=os.getenv(f"{prefix}_ENDPOINT"),
        api_key=os.getenv(f"{prefix}_KEY") or os.getenv(f"{prefix}_API_KEY"),
        api_version=os.getenv(f"{prefix}_API_VERSION"),
    )


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value
