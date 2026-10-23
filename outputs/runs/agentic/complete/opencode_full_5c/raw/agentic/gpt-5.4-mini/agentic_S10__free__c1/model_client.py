import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Iterable, Optional

from openai import OpenAI


DEFAULT_MODEL_FAMILY = "gpt-5.4-mini"


@dataclass
class ModelConfig:
    api_key: Optional[str] = None
    model: str = DEFAULT_MODEL_FAMILY
    base_url: Optional[str] = None


def load_config(model: Optional[str] = None) -> ModelConfig:
    return ModelConfig(
        api_key=os.getenv("OPENAI_API_KEY"),
        model=model or os.getenv("OPENAI_MODEL", DEFAULT_MODEL_FAMILY),
        base_url=os.getenv("OPENAI_BASE_URL"),
    )


def get_client(config: Optional[ModelConfig] = None) -> OpenAI:
    cfg = config or load_config()
    kwargs: Dict[str, Any] = {}
    if cfg.api_key:
        kwargs["api_key"] = cfg.api_key
    if cfg.base_url:
        kwargs["base_url"] = cfg.base_url
    return OpenAI(**kwargs)


def normalize_messages(
    system: str, user: str, extra: Optional[Iterable[Dict[str, str]]] = None
):
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    if extra:
        messages.extend(list(extra))
    messages.append({"role": "user", "content": user})
    return messages


def text_from_response(response: Any) -> str:
    if hasattr(response, "output_text") and response.output_text:
        return response.output_text
    try:
        return response.output[0].content[0].text
    except Exception:
        return ""


def safe_json_loads(text: str) -> Dict[str, Any]:
    return json.loads(text)
