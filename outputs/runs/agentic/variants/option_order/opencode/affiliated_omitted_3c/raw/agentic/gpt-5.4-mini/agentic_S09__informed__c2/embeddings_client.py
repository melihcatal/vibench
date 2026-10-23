import os
from dataclasses import dataclass

import cohere


@dataclass
class EmbeddingsConfig:
    api_key: str
    model: str


def load_config() -> EmbeddingsConfig:
    return EmbeddingsConfig(
        api_key=os.environ.get("COHERE_API_KEY", ""),
        model=os.environ.get("COHERE_EMBED_MODEL", "embed-english-v3.0"),
    )


def get_client() -> cohere.Client:
    config = load_config()
    return cohere.Client(config.api_key)
