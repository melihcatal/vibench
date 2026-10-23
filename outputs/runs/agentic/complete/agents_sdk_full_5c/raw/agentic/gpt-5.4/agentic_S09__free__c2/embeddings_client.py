from __future__ import annotations

import os
from openai import OpenAI

DEFAULT_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")


def get_embeddings_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY is required")
    return OpenAI(api_key=api_key, base_url=OPENAI_BASE_URL)


def resolve_embedding_model(model: str | None = None) -> str:
    return model or DEFAULT_EMBEDDING_MODEL
