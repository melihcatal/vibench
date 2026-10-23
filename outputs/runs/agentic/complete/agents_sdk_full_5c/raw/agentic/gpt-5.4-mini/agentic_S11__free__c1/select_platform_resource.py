from __future__ import annotations

from typing import Optional

from openai import OpenAI

from model_client import DEFAULT_MODEL, get_client


def select_platform_resource(preferred: Optional[str] = None, client: Optional[OpenAI] = None) -> str:
    client = client or get_client()
    _ = client.models.list()
    return preferred or DEFAULT_MODEL
