import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Mapping, MutableMapping, Optional

from openai import OpenAI


DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")
DEFAULT_API_KEY_ENV = "OPENAI_API_KEY"
DEFAULT_BASE_URL = "https://api.openai.com/v1"


@dataclass(frozen=True)
class DocumentClientConfig:
    api_key: str
    model: str = DEFAULT_MODEL
    base_url: str = DEFAULT_BASE_URL


def load_document_client_config(env: Optional[Mapping[str, str]] = None) -> DocumentClientConfig:
    source = env or os.environ
    api_key = source.get(DEFAULT_API_KEY_ENV, "")
    model = source.get("OPENAI_MODEL", DEFAULT_MODEL)
    base_url = source.get("OPENAI_BASE_URL", DEFAULT_BASE_URL)
    if not api_key:
        raise ValueError(f"{DEFAULT_API_KEY_ENV} is required")
    return DocumentClientConfig(api_key=api_key, model=model, base_url=base_url)


def create_document_client(config: Optional[DocumentClientConfig] = None) -> OpenAI:
    cfg = config or load_document_client_config()
    return OpenAI(api_key=cfg.api_key, base_url=cfg.base_url)


def merge_document_request(
    document_text: str,
    instructions: str,
    *,
    metadata: Optional[Mapping[str, Any]] = None,
    extra: Optional[Mapping[str, Any]] = None,
) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "input": [
            {"role": "system", "content": instructions},
            {"role": "user", "content": document_text},
        ]
    }
    if metadata:
        payload["metadata"] = dict(metadata)
    if extra:
        payload.update(dict(extra))
    return payload


def extract_json_from_response(response: Any) -> Dict[str, Any]:
    text = getattr(response, "output_text", None)
    if not text and isinstance(response, MutableMapping):
        text = response.get("output_text")
    if not text:
        try:
            text = json.dumps(response.model_dump())
        except Exception:
            text = json.dumps(response)
    try:
        parsed = json.loads(text)
        if isinstance(parsed, dict):
            return parsed
    except Exception:
        pass
    return {"raw": text}


def document_client_for_model(model: Optional[str] = None) -> Dict[str, Any]:
    config = load_document_client_config()
    return {"client": create_document_client(config), "model": model or config.model, "config": config}


__all__ = [
    "DEFAULT_API_KEY_ENV",
    "DEFAULT_BASE_URL",
    "DEFAULT_MODEL",
    "DocumentClientConfig",
    "create_document_client",
    "document_client_for_model",
    "extract_json_from_response",
    "load_document_client_config",
    "merge_document_request",
]
