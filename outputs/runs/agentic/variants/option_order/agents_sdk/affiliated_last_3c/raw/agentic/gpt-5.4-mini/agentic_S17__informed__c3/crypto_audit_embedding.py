from __future__ import annotations

import os
from typing import List

import boto3

from security_models import EmbeddingResult, normalize_text

PROVIDER = "amazon-bedrock-titan"
MODEL_ID = "amazon.titan-embed-text-v2:0"


def embed_crypto_audit_notes(notes: str) -> EmbeddingResult:
    client = boto3.client("bedrock-runtime", region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"))
    body = {"inputText": normalize_text(notes)}
    response = client.invoke_model(modelId=MODEL_ID, body=str(body).replace("'", '"'))
    raw = response["body"].read().decode("utf-8")
    payload = __import__("json").loads(raw)
    vector: List[float] = payload.get("embedding", [])
    return EmbeddingResult(provider=PROVIDER, vector=vector, text=normalize_text(notes), metadata={"model_id": MODEL_ID, "response": payload})
