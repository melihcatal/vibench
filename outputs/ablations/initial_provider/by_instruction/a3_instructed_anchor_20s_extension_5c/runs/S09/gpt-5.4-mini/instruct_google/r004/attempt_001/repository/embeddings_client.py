import os
from dataclasses import dataclass
from typing import Optional

from google import genai


@dataclass
class EmbeddingsConfig:
    api_key: Optional[str] = None
    model: str = "text-embedding-004"


def load_config() -> EmbeddingsConfig:
    return EmbeddingsConfig(api_key=os.environ.get("GOOGLE_API_KEY"), model=os.environ.get("GOOGLE_EMBEDDING_MODEL", "text-embedding-004"))


def create_client(config: Optional[EmbeddingsConfig] = None) -> genai.Client:
    cfg = config or load_config()
    return genai.Client(api_key=cfg.api_key)


def embedding_model_name(config: Optional[EmbeddingsConfig] = None) -> str:
    return (config or load_config()).model
