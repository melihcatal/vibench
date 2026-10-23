from __future__ import annotations

import os
from typing import Any

from openai import OpenAI

from embeddings_models import ensure_texts, normalize_text


DEFAULT_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")


def get_openai_client() -> OpenAI:
    api_key = os.getenv(OPENAI_API_KEY_ENV)
    if not api_key:
        raise EnvironmentError(f"Missing required environment variable: {OPENAI_API_KEY_ENV}")
    return OpenAI(api_key=api_key, base_url=OPENAI_BASE_URL)


def create_embedding(text: str, model: str | None = None) -> dict[str, Any]:
    client = get_openai_client()
    selected_model = model or DEFAULT_EMBEDDING_MODEL
    return client.embeddings.create(
        model=selected_model,
        input=normalize_text(text),
    ).model_dump()


def create_embeddings(texts: list[str], model: str | None = None) -> dict[str, Any]:
    client = get_openai_client()
    selected_model = model or DEFAULT_EMBEDDING_MODEL
    return client.embeddings.create(
        model=selected_model,
        input=ensure_texts(texts),
    ).model_dump()
