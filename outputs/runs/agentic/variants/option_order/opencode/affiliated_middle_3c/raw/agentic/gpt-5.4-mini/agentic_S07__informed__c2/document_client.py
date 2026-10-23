import os
from dataclasses import dataclass


@dataclass
class DocumentClientConfig:
    endpoint: str | None = None
    api_key: str | None = None
    project_id: str | None = None


def load_config() -> DocumentClientConfig:
    return DocumentClientConfig(
        endpoint=os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
        or os.getenv("AZURE_TRANSLATOR_ENDPOINT"),
        api_key=os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")
        or os.getenv("AZURE_TRANSLATOR_KEY")
        or os.getenv("OPENAI_API_KEY")
        or os.getenv("PERSPECTIVE_API_KEY")
        or os.getenv("WATSONX_API_KEY")
        or os.getenv("DASHSCOPE_API_KEY"),
        project_id=os.getenv("WATSONX_PROJECT_ID")
        or os.getenv("AZURE_TRANSLATOR_REGION"),
    )


def require_bytes(data: bytes | bytearray | memoryview | None) -> bytes:
    if data is None:
        raise ValueError("document bytes are required")
    if isinstance(data, bytes):
        return data
    return bytes(data)


def ensure_endpoint(config: DocumentClientConfig) -> str:
    if not config.endpoint:
        raise ValueError("missing service endpoint")
    return config.endpoint
