from __future__ import annotations

from typing import List, Optional

from openai import OpenAI

from model_client import get_client, get_model_name


_PROVIDER = "openai"
_DEFAULT_EMBED_MODEL = "text-embedding-3-small"


def output_embedding(text: str, *, client: Optional[OpenAI] = None, model: Optional[str] = None) -> List[float]:
    """Embed model outputs for clustering or retrieval using OpenAI embeddings."""
    model_name = model or get_model_name("output_embedding", _DEFAULT_EMBED_MODEL)
    api_client = client or get_client(provider=_PROVIDER)
    response = api_client.embeddings.create(model=model_name, input=text)
    return list(response.data[0].embedding)
