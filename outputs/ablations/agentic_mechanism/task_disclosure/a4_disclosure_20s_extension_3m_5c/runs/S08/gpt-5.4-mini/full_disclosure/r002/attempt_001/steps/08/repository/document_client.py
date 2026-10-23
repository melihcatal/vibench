import os
from dataclasses import dataclass
from typing import Any, Dict, Mapping, Optional

try:
    from openai import OpenAI
except Exception as exc:  # pragma: no cover
    OpenAI = None
    _OPENAI_IMPORT_ERROR = exc
else:
    _OPENAI_IMPORT_ERROR = None


DEFAULT_MODEL = os.getenv("STRUCTURED_DOCUMENT_MODEL", "openai/gpt-5.4-mini")
DEFAULT_ENDPOINT = os.getenv("STRUCTURED_DOCUMENT_BASE_URL", "https://api.openai.com/v1")


@dataclass(frozen=True)
class DocumentClientConfig:
    api_key: str
    base_url: str = DEFAULT_ENDPOINT
    model: str = DEFAULT_MODEL


def load_document_client_config(env: Mapping[str, str] = os.environ) -> DocumentClientConfig:
    api_key = env.get("OPENAI_API_KEY") or env.get("STRUCTURED_DOCUMENT_API_KEY")
    if not api_key:
        raise ValueError("Missing OPENAI_API_KEY or STRUCTURED_DOCUMENT_API_KEY")
    return DocumentClientConfig(
        api_key=api_key,
        base_url=env.get("STRUCTURED_DOCUMENT_BASE_URL", DEFAULT_ENDPOINT),
        model=env.get("STRUCTURED_DOCUMENT_MODEL", DEFAULT_MODEL),
    )


def create_document_client(config: Optional[DocumentClientConfig] = None) -> Any:
    if OpenAI is None:
        raise ImportError("openai is required for structured document extraction") from _OPENAI_IMPORT_ERROR
    cfg = config or load_document_client_config()
    return OpenAI(api_key=cfg.api_key, base_url=cfg.base_url)


def get_document_model(config: Optional[DocumentClientConfig] = None) -> str:
    return (config or load_document_client_config()).model


def document_response_format(schema: Dict[str, Any]) -> Dict[str, Any]:
    return {"type": "json_schema", "json_schema": {"name": "structured_document_extraction", "schema": schema, "strict": True}}


def extract_json_content(response: Any) -> Dict[str, Any]:
    content = response.choices[0].message.content
    if isinstance(content, dict):
        return content
    if not content:
        return {}
    import json

    return json.loads(content)
