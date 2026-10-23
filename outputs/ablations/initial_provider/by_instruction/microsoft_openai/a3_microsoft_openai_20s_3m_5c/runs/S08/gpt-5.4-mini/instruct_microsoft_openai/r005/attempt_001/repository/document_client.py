import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from openai import OpenAI


@dataclass
class DocumentClientConfig:
    api_key: Optional[str] = None
    model: str = "gpt-5.4-mini"
    base_url: Optional[str] = None


def load_config() -> DocumentClientConfig:
    return DocumentClientConfig(
        api_key=os.getenv("OPENAI_API_KEY"),
        model=os.getenv("OPENAI_MODEL", "gpt-5.4-mini"),
        base_url=os.getenv("OPENAI_BASE_URL"),
    )


def create_client(config: Optional[DocumentClientConfig] = None) -> OpenAI:
    cfg = config or load_config()
    kwargs: Dict[str, Any] = {}
    if cfg.api_key:
        kwargs["api_key"] = cfg.api_key
    if cfg.base_url:
        kwargs["base_url"] = cfg.base_url
    return OpenAI(**kwargs)


def extract_json_schema_response(client: OpenAI, model: str, prompt: str, schema: Dict[str, Any]) -> Dict[str, Any]:
    response = client.responses.create(
        model=model,
        input=prompt,
        text={"format": {"type": "json_schema", "name": "document_extraction", "schema": schema, "strict": True}},
    )
    text = response.output_text
    return __import__("json").loads(text)
