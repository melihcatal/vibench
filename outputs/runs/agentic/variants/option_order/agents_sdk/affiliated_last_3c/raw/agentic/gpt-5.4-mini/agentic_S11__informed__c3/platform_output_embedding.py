"""Embed platform outputs for evaluation or retrieval using OpenAI embeddings.

Provider: OpenAI / Azure OpenAI embeddings via openai.
Environment: OPENAI_API_KEY.
"""

from __future__ import annotations

import os

from openai import OpenAI

from model_models import EmbeddedOutput


def embed_platform_output(text: str) -> EmbeddedOutput:
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    client = OpenAI(api_key=api_key)
    result = client.embeddings.create(model="text-embedding-3-small", input=text)
    vector = result.data[0].embedding
    return EmbeddedOutput(text=text, vector=list(vector), model=result.model)
