import os
from dataclasses import dataclass
from typing import Any, Dict

from openai import OpenAI


@dataclass
class EmbeddingsConfig:
    api_key: str
    base_url: str
    model: str


def load_config() -> EmbeddingsConfig:
    return EmbeddingsConfig(
        api_key=os.environ.get("OPENAI_API_KEY", ""),
        base_url=os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        model=os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"),
    )


def make_client() -> OpenAI:
    cfg = load_config()
    return OpenAI(api_key=cfg.api_key or None, base_url=cfg.base_url)


def embedding_request(model: str, input_data: Any) -> Dict[str, Any]:
    return {"model": model, "input": input_data}
