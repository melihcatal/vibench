from __future__ import annotations

from typing import Dict

from openai.types import CreateEmbeddingResponse

from security_client import OPENAI_PROVIDER, get_openai_client
from security_models import EmbeddingResult


def crypto_audit_embedding(
    text: str, model: str = "text-embedding-3-large"
) -> Dict[str, object]:
    client = get_openai_client()
    response: CreateEmbeddingResponse = client.embeddings.create(
        model=model,
        input=text,
    )
    vector = response.data[0].embedding
    result = EmbeddingResult(
        provider=OPENAI_PROVIDER,
        model=model,
        vector=vector,
        dimensions=len(vector),
        input_text=text,
    )
    return result.to_dict()
