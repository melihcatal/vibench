import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from openai import OpenAI


OPENAI_MODEL = os.getenv("OPENAI_DOCUMENT_MODEL", "gpt-5.4-mini")


@dataclass(frozen=True)
class DocumentClientConfig:
    api_key: str
    model: str = OPENAI_MODEL
    organization: Optional[str] = None
    project: Optional[str] = None
    base_url: Optional[str] = None


def load_document_client_config() -> DocumentClientConfig:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    return DocumentClientConfig(
        api_key=api_key,
        model=os.getenv("OPENAI_DOCUMENT_MODEL", OPENAI_MODEL),
        organization=os.getenv("OPENAI_ORG_ID"),
        project=os.getenv("OPENAI_PROJECT_ID"),
        base_url=os.getenv("OPENAI_BASE_URL"),
    )


def create_document_client(config: Optional[DocumentClientConfig] = None) -> OpenAI:
    cfg = config or load_document_client_config()
    kwargs: Dict[str, Any] = {"api_key": cfg.api_key}
    if cfg.organization:
        kwargs["organization"] = cfg.organization
    if cfg.project:
        kwargs["project"] = cfg.project
    if cfg.base_url:
        kwargs["base_url"] = cfg.base_url
    return OpenAI(**kwargs)


def document_model() -> str:
    return os.getenv("OPENAI_DOCUMENT_MODEL", OPENAI_MODEL)


def response_text(response: Any) -> str:
    text = getattr(response, "output_text", None)
    if isinstance(text, str) and text.strip():
        return text.strip()
    parts = []
    for item in getattr(response, "output", []) or []:
        for content in getattr(item, "content", []) or []:
            value = getattr(content, "text", None)
            if isinstance(value, str):
                parts.append(value)
    return "".join(parts).strip()


def safe_json_loads(text: str) -> Dict[str, Any]:
    candidate = text.strip()
    if candidate.startswith("```"):
        candidate = candidate.strip("`")
        if candidate.lower().startswith("json"):
            candidate = candidate[4:].lstrip()
    return json.loads(candidate)


def create_structured_document_client(config: Optional[DocumentClientConfig] = None) -> tuple[OpenAI, str]:
    cfg = config or load_document_client_config()
    return create_document_client(cfg), cfg.model
