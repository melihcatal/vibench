from __future__ import annotations

from typing import Any, Dict

from openai import OpenAI

from security_models import AuditEmbeddingResult, sha256_text


def crypto_audit_embedding(payload: Dict[str, Any]) -> Dict[str, Any]:
    note = str(payload["note"])
    model = payload.get("model", "text-embedding-3-large")
    client = OpenAI(api_key=payload.get("openai_api_key"))
    response = client.embeddings.create(model=model, input=note)
    vector = list(response.data[0].embedding)
    result = AuditEmbeddingResult(
        provider="openai",
        model=model,
        vector=vector,
        dimensions=len(vector),
        note_sha256=sha256_text(note),
    )
    return result.to_dict()
