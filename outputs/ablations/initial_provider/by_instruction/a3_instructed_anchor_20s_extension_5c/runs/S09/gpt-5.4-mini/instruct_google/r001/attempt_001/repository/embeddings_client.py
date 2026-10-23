import os
from dataclasses import dataclass

from google import genai


@dataclass
class EmbeddingsConfig:
    api_key: str
    model: str = "text-embedding-004"


def load_config() -> EmbeddingsConfig:
    api_key = os.getenv("GOOGLE_API_KEY", "")
    model = os.getenv("GOOGLE_EMBEDDING_MODEL", "text-embedding-004")
    return EmbeddingsConfig(api_key=api_key, model=model)


def get_client() -> genai.Client:
    config = load_config()
    return genai.Client(api_key=config.api_key)
