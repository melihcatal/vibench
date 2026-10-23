from __future__ import annotations

from security_client import get_bedrock_runtime_client
from security_models import EmbeddingResponse, compact_json


BEDROCK_EMBED_MODEL = "amazon.titan-embed-text-v2:0"


def embed_crypto_audit_notes(text: str) -> EmbeddingResponse:
    bedrock = get_bedrock_runtime_client()
    body = compact_json({"inputText": text})
    response = bedrock.invoke_model(
        modelId=BEDROCK_EMBED_MODEL,
        body=body,
        contentType="application/json",
        accept="application/json",
    )
    payload = response["body"].read().decode("utf-8")
    data = __import__("json").loads(payload)
    vector = data["embedding"]
    return EmbeddingResponse(
        provider="amazon-bedrock",
        model=BEDROCK_EMBED_MODEL,
        vector=vector,
        dimensions=len(vector),
    )
