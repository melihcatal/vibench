from __future__ import annotations

from typing import Optional

from speech_client import get_openai_client, resolve_embedding_model
from speech_models import EmbeddingResult


def embed_script(
    script_text: str, model: Optional[str] = None, api_key: Optional[str] = None
) -> EmbeddingResult:
    resolved_model = resolve_embedding_model(model)
    client = get_openai_client(api_key)
    response = client.embeddings.create(model=resolved_model, input=script_text)
    return EmbeddingResult(embedding=response.data[0].embedding, model=resolved_model)
