import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional

from openai import OpenAI


OPENAI_MODEL = "gpt-5.4-mini"


@dataclass
class DocumentClientConfig:
    api_key: Optional[str] = None
    model: str = OPENAI_MODEL

    @classmethod
    def from_env(cls) -> "DocumentClientConfig":
        return cls(api_key=os.environ.get("OPENAI_API_KEY"), model=os.environ.get("DOCUMENT_EXTRACTION_MODEL", OPENAI_MODEL))


def load_local_config(path: str = "document_client.json") -> DocumentClientConfig:
    if not os.path.isfile(path):
        return DocumentClientConfig.from_env()
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return DocumentClientConfig(api_key=data.get("api_key") or os.environ.get("OPENAI_API_KEY"), model=data.get("model") or os.environ.get("DOCUMENT_EXTRACTION_MODEL", OPENAI_MODEL))


def build_openai_client(config: Optional[DocumentClientConfig] = None) -> OpenAI:
    cfg = config or load_local_config()
    return OpenAI(api_key=cfg.api_key)


def _normalize_fields(fields: Iterable[str]) -> List[str]:
    return [field.strip() for field in fields if field and field.strip()]


def _parse_json_text(text: str) -> Dict[str, Any]:
    text = text.strip()
    if not text:
        return {}
    try:
        parsed = json.loads(text)
        return parsed if isinstance(parsed, dict) else {"result": parsed}
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            parsed = json.loads(text[start : end + 1])
            return parsed if isinstance(parsed, dict) else {"result": parsed}
        raise


class DocumentClient:
    def __init__(self, config: Optional[DocumentClientConfig] = None):
        self.config = config or load_local_config()
        self.client = build_openai_client(self.config)

    def extract_structured_document(self, document_text: str, required_fields: Optional[Iterable[str]] = None) -> Dict[str, Any]:
        instruction = "Extract structured fields from the document and return strict JSON only."
        fields = _normalize_fields(required_fields or [])
        if fields:
            instruction = f"Extract these fields from the document: {', '.join(fields)}. Return strict JSON only."
        response = self.client.responses.create(
            model=self.config.model,
            input=f"{instruction}\n\nDocument:\n{document_text}",
            temperature=0,
        )
        return _parse_json_text(response.output_text)


def get_document_client(config_path: str = "document_client.json") -> DocumentClient:
    return DocumentClient(load_local_config(config_path))
